# Server-Side Request Forgery (SSRF) Prevention & Safe Egress

Server-Side Request Forgery (**SSRF**, OWASP API7 / A10) allows an attacker to coerce the backend server into sending unauthorized network requests to internal services, private networks, loopback addresses, or cloud metadata instances.

---

## 1. Primary SSRF Sinks in Application Code

Audit every place where the application receives a URL or host from user input:
- **Webhooks & Subscriptions:** User-configured event notifications.
- **File & Image Importers:** `fetch(avatarUrl)`, `downloadReport(url)`.
- **HTML-to-PDF Generators:** Puppeteer, wkhtmltopdf, Playwright rendering user HTML containing `<iframe src="http://169.254.169.254/latest/meta-data/">` or `<img src="...">`.
- **Remote Resource Loaders:** RSS readers, oEmbed consumers, URL unfurlers.
- **XML Processors:** Parsers resolving external DTDs or entities (XXE).

---

## 2. Why Naive Defenses Fail

### ❌ Failure Mode 1: Domain Blacklists / Regex
Attackers easily bypass regex checks:
- Octal / Hex IP notation: `http://0177.0.0.1` or `http://0x7f000001` $\rightarrow$ resolves to `127.0.0.1`.
- Integer notation: `http://2130706433` $\rightarrow$ resolves to `127.0.0.1`.
- Subdomain trickery: `http://169.254.169.254.nip.io`.
- URL parsing differences: `http://attacker.com#@trusted.com`.

### ❌ Failure Mode 2: Time-of-Check to Time-of-Use (DNS Rebinding)
1. Application resolves `webhook.attacker.com` $\rightarrow$ DNS returns `93.184.216.34` (Public IP, passes validation).
2. Application calls `fetch("http://webhook.attacker.com")` $\rightarrow$ Second DNS lookup occurs (due to TTL=0) $\rightarrow$ DNS returns `169.254.169.254` (Private cloud metadata).
3. The server requests cloud metadata and leaks IAM instance profile tokens.

---

## 3. The Defense-in-Depth Solution: Safe Egress Client

A secure HTTP client must implement **Pre-Flight DNS Resolution and IP Pinning**:

1. **Parse & Validate Protocol:** Allow only `http:` and `https:`.
2. **Resolve DNS to IP Address:** Query system DNS explicitly.
3. **Validate IP Address Against Forbidden Ranges:**
   - `0.0.0.0/8` (Current network)
   - `10.0.0.0/8` (RFC 1918 Private)
   - `127.0.0.0/8` (Loopback)
   - `169.254.0.0/16` (Link-local & Cloud Metadata: AWS/GCP/Azure)
   - `172.16.0.0/12` (RFC 1918 Private)
   - `192.168.0.0/16` (RFC 1918 Private)
   - `::1/128`, `fc00::/7`, `fe80::/10` (IPv6 loopback, ULA, link-local)
4. **Connect Directly to the Validated IP Address:**
   - Overwrite the socket connection destination with the pinned IP address while keeping the original `Host` header for TLS SNI and virtual hosting.
5. **Handle HTTP Redirects Safely:**
   - Never follow redirects blindly (`redirect: "manual"` or validate each hop through steps 1-4).

---

## 4. Cloud Metadata Hardening
- **AWS:** Enforce IMDSv2 (`aws ec2 modify-instance-metadata-options --http-tokens required --http-put-response-hop-limit 1`).
- **GCP:** Ensure `Metadata-Flavor: Google` header requirement is never bypassable by attacker parameters.
- **Egress Firewall:** Restrict outbound traffic from application pods to only necessary CIDRs via Kubernetes NetworkPolicies.
