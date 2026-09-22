/**
 * Production-Ready SSRF-Safe Fetch Client (TypeScript / Node.js)
 * Implements Pre-Flight DNS Resolution, IP Pinning, and Egress Boundary Filtering.
 */

import * as dns from "node:dns/promises";
import * as http from "node:http";
import * as https from "node:https";
import * as net from "node:net";
import { URL } from "node:url";

// Forbidden CIDR ranges (RFC 1918, RFC 3927 Link-Local, Loopback, Cloud Metadata)
const FORBIDDEN_IPV4_RANGES = [
  { start: "0.0.0.0", end: "0.255.255.255" },       // Current network
  { start: "10.0.0.0", end: "10.255.255.255" },     // RFC 1918 Private
  { start: "127.0.0.0", end: "127.255.255.255" },   // Loopback
  { start: "169.254.0.0", end: "169.254.255.255" }, // Link-local & Cloud Metadata (AWS/GCP)
  { start: "172.16.0.0", end: "172.31.255.255" },   // RFC 1918 Private
  { start: "192.168.0.0", end: "192.168.255.255" }, // RFC 1918 Private
  { start: "224.0.0.0", end: "239.255.255.255" },   // Multicast
];

function ipToNumber(ip: string): number {
  return ip
    .split(".")
    .reduce((acc, octet) => (acc << 8) + parseInt(octet, 10), 0) >>> 0;
}

export function isForbiddenIp(ip: string): boolean {
  if (!net.isIP(ip)) return true;

  if (net.isIPv4(ip)) {
    const num = ipToNumber(ip);
    for (const range of FORBIDDEN_IPV4_RANGES) {
      if (num >= ipToNumber(range.start) && num <= ipToNumber(range.end)) {
        return true;
      }
    }
    return false;
  }

  // IPv6: Block loopback (::1), link-local (fe80::/10), unique local (fc00::/7)
  const lower = ip.toLowerCase();
  if (lower === "::1" || lower.startsWith("fe80:") || lower.startsWith("fc00:") || lower.startsWith("fd")) {
    return true;
  }

  return false;
}

export interface SafeFetchOptions {
  timeoutMs?: number;
  maxRedirects?: number;
  allowedProtocols?: string[];
}

/**
 * Safely fetches an outbound URL, protecting against SSRF and DNS rebinding attacks.
 */
export async function safeFetch(
  rawUrl: string,
  options: SafeFetchOptions = {}
): Promise<{ status: number; headers: http.IncomingHttpHeaders; body: string }> {
  const { timeoutMs = 5000, maxRedirects = 3, allowedProtocols = ["http:", "https:"] } = options;

  let currentUrl = new URL(rawUrl);
  let redirectCount = 0;

  while (redirectCount <= maxRedirects) {
    if (!allowedProtocols.includes(currentUrl.protocol)) {
      throw new Error(`SSRF Block: Protocol ${currentUrl.protocol} is forbidden.`);
    }

    // 1. Pre-flight DNS resolution
    const addresses = await dns.resolve4(currentUrl.hostname).catch(async () => {
      return await dns.resolve6(currentUrl.hostname);
    });

    if (!addresses || addresses.length === 0) {
      throw new Error(`DNS Resolution failed for host: ${currentUrl.hostname}`);
    }

    const resolvedIp = addresses[0];

    // 2. Validate IP against forbidden ranges
    if (isForbiddenIp(resolvedIp)) {
      throw new Error(
        `🚨 SSRF Blocked: Host '${currentUrl.hostname}' resolved to forbidden private/metadata IP '${resolvedIp}'.`
      );
    }

    // 3. Connect via pinned IP address while keeping the Host header
    const protocolModule = currentUrl.protocol === "https:" ? https : http;
    const port = currentUrl.port || (currentUrl.protocol === "https:" ? 443 : 80);

    const response = await new Promise<{
      status: number;
      headers: http.IncomingHttpHeaders;
      body: string;
      redirectUrl?: string;
    }>((resolve, reject) => {
      const req = protocolModule.request(
        {
          host: resolvedIp, // Pinned IP prevents DNS rebinding
          port: port,
          path: currentUrl.pathname + currentUrl.search,
          method: "GET",
          headers: {
            Host: currentUrl.host, // Necessary for SNI and virtual hosting
            "User-Agent": "AppSec-SafeClient/1.0",
          },
          timeout: timeoutMs,
          servername: currentUrl.hostname, // TLS SNI handshake
        },
        (res) => {
          let body = "";
          res.setEncoding("utf-8");
          res.on("data", (chunk) => {
            body += chunk;
          });
          res.on("end", () => {
            const statusCode = res.statusCode || 0;
            if (statusCode >= 300 && statusCode < 400 && res.headers.location) {
              const nextUrl = new URL(res.headers.location, currentUrl.href).href;
              resolve({ status: statusCode, headers: res.headers, body, redirectUrl: nextUrl });
            } else {
              resolve({ status: statusCode, headers: res.headers, body });
            }
          });
        }
      );

      req.on("timeout", () => {
        req.destroy();
        reject(new Error(`Connection timed out after ${timeoutMs}ms`));
      });

      req.on("error", reject);
      req.end();
    });

    if (response.redirectUrl) {
      redirectCount++;
      currentUrl = new URL(response.redirectUrl);
      continue;
    }

    return {
      status: response.status,
      headers: response.headers,
      body: response.body,
    };
  }

  throw new Error(`Exceeded maximum redirects limit of ${maxRedirects}`);
}
