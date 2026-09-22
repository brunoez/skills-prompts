# OWASP API Security Testing Framework (ASTF) & API Top 10 Reference

This reference outlines the technical audit procedures for modern web APIs (REST, GraphQL, gRPC, and LLM endpoints) based on **OWASP API Security Top 10 2023**, **WSTG v4.2**, and **OWASP ASVS v4.0.3**.

---

## 1. The 10 Primary API Vulnerability Categories (OWASP 2023)

### API1:2023 – Broken Object Level Authorization (BOLA / IDOR)
* **ASVS:** V13.1.1, V13.1.3 (L2) | **CWE:** CWE-639
* **Root Cause:** Relying solely on client-provided IDs (`/api/documents/{id}`, `/users/{uuid}/profile`) without enforcing tenancy/ownership in database queries.
* **Audit Rule:**
  ```typescript
  // ❌ VULNERABLE: Direct lookup without tenancy scope
  const invoice = await db.invoices.findUnique({ where: { id: req.params.id } });
  
  // ✅ SECURE: Tenancy scope enforced in database query
  const invoice = await db.invoices.findFirst({
    where: { id: req.params.id, organizationId: req.user.organizationId }
  });
  ```

### API2:2023 – Broken Authentication
* **ASVS:** V2.1, V3.1 (L2) | **WSTG:** WSTG-SESS-03, IDNT-04 | **CWE:** CWE-287
* **Root Cause:** Missing authentication checks on sensitive routes, weak JWT signature checks (`alg: none`), lack of token revocation, or predictable tokens.
* **Audit Rule:** Reject tokens with symmetric key confusion (`HS256` signed by public key of `RS256`), verify expiration (`exp`), and check revocation blacklist.

### API3:2023 – Broken Object Property Level Authorization (BOPLA)
* **ASVS:** V13.1.4, V13.2.1 (L2) | **CWE:** CWE-915 (Mass Assignment), CWE-213 (Excessive Exposure)
* **Root Cause:**
  1. *Mass Assignment:* Accepting arbitrary JSON properties into database updates (e.g. `role: "admin"`, `verified: true`, `balance: 99999`).
  2. *Excessive Exposure:* Returning database entities directly without an explicit response DTO/serializer, exposing password hashes, internal IDs, or PII.
* **Audit Rule:**
  ```typescript
  // ✅ Enforce strict schema stripping (e.g. Zod strict mode)
  const UpdateProfileSchema = z.object({
    displayName: z.string().min(2).max(50),
    bio: z.string().max(200).optional()
  }).strict();
  ```

### API4:2023 – Unrestricted Resource Consumption
* **ASVS:** V13.1.5, V13.2.3 (L2) | **CWE:** CWE-770
* **Root Cause:** Missing rate limiting, unbounded pagination (`limit=999999`), missing request body size caps, missing execution timeouts.
* **Audit Rule:** Default pagination with maximum hard ceiling (`Math.min(requestedLimit, 100)`), middleware rate limiting by IP/User, body size limit (`express.json({ limit: '1mb' })`).

### API5:2023 – Broken Function Level Authorization (BFLA)
* **ASVS:** V4.1.1, V13.1.1 (L2) | **WSTG:** WSTG-ATHZ-01 | **CWE:** CWE-285
* **Root Cause:** Administrative or privileged endpoints accessible by regular users; method-tampering bypass (e.g. `PUT /api/users/promote` lacking RBAC check).
* **Audit Rule:** Centralized policy enforcement (e.g. CASL, Open Policy Agent, or explicit role guard middlewares) declared at the route level.

### API6:2023 – Unrestricted Access to Sensitive Business Flows
* **ASVS:** V11.1.1 (L2) | **CWE:** CWE-799
* **Root Cause:** Checkout race conditions (TOCTOU), voucher re-use, automated credential stuffing, or buying goods without idempotency keys.
* **Audit Rule:** Distributed locks (Redis Redlock), transactional database locks (`SELECT ... FOR UPDATE`), and required `Idempotency-Key` headers.

### API7:2023 – Server-Side Request Forgery (SSRF)
* **ASVS:** V12.6.1 (L2) | **CWE:** CWE-918
* **Root Cause:** Fetching remote URLs supplied by users (webhooks, avatar uploads from URL, PDF rendering) without IP allow-listing and DNS rebinding protection.
* **Audit Rule:** Inspect DNS response *before* opening TCP sockets. Block RFC 1918, `127.0.0.1`, `169.254.169.254`, and IPv6 equivalents.

### API8:2023 – Security Misconfiguration
* **ASVS:** V14.1.1, V14.4.1 (L2) | **WSTG:** WSTG-CLNT-07 | **CWE:** CWE-16
* **Root Cause:** Wildcard CORS (`Access-Control-Allow-Origin: *` with credentials), missing security headers (`HSTS`, `nosniff`, `CSP`), verbose error stack traces in production.
* **Audit Rule:** Environment-driven error handlers that log stack traces internally but return an opaque correlation ID to the client.

### API9:2023 – Improper Inventory Management
* **ASVS:** V13.2.2, V14.2.1 (L2) | **CWE:** CWE-1059
* **Root Cause:** Shadow APIs (`/api/v1/` still active without authentication while `/api/v2/` is patched), internal staging endpoints exposed to the internet, spec drift.
* **Audit Rule:** Automated contract drift checks comparing OpenAPI specs against actual routing tables.

### API10:2023 – Unsafe Consumption of APIs
* **ASVS:** V13.2.5, V13.2.6 (L2) | **CWE:** CWE-20
* **Root Cause:** Trusting third-party APIs or webhooks blindly without validating schemas, redirecting to unvalidated downstream URLs, or failing to verify webhook HMAC signatures.
* **Audit Rule:** Verify webhook cryptographic signature (`X-Hub-Signature-256`) before parsing payload; validate downstream data with Zod schemas.

---

## 2. Modern Protocol Extensions

### GraphQL Security
1. **Introspection in Production:** Disable `introspection: false` in production schemas.
2. **Query Depth Limiting:** Enforce a max depth limit (e.g. 5-7 levels) using `graphql-depth-limit`.
3. **Query Cost Analysis:** Calculate query complexity points before execution to prevent circular relationship DoS (`user { posts { author { posts ... } } }`).

### gRPC Security
1. **Server Reflection:** Disable `grpc.reflection.v1alpha.ServerReflection` in production.
2. **Unary/Stream Interceptors:** Ensure every RPC method executes authentication and tenancy interceptors before business logic.
3. **Max Message Size:** Enforce limits on inbound streams (`grpc.max_receive_message_length`).

### AI / LLM API Endpoints
1. **Indirect Prompt Injection:** Validate and isolate data originating from external webhooks/documents before feeding into LLM system prompts.
2. **Excessive Agency:** Restrict tools exposed to the agent to read-only or scoped operations; require human-in-the-loop or System 1 guardrails for destructive calls.
