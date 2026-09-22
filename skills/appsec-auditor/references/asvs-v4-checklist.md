# OWASP ASVS v4.0.3 Verification Checklist (Level 2 Benchmark)

The **OWASP Application Security Verification Standard (ASVS v4.0.3)** provides an open, rigorous framework for verifying technical application security controls. This checklist focuses on **Level 2 (Standard Enterprise Applications)**.

---

## V1: Architecture, Design and Threat Modeling
- [ ] **V1.1.1 (L2):** Verify that all application components and third-party dependencies are documented and tracked in a Software Bill of Materials (SBOM).
- [ ] **V1.4.1 (L2):** Verify that trust boundaries are documented, separating untrusted client inputs from trusted backend services and databases.
- [ ] **V1.14.1 (L2):** Verify that all machine learning and AI components are audited against model poisoning, prompt injection, and excessive agency.

---

## V2: Authentication Verification Requirements
- [ ] **V2.1.1 (L2):** Verify that user passwords are hashed using **Argon2id** (memory $\ge$ 64MB, iterations $\ge$ 3) or bcrypt (cost $\ge$ 12).
- [ ] **V2.1.7 (L2):** Verify that password submission supports at least 64 characters and does not arbitrarily restrict special characters.
- [ ] **V2.2.1 (L2):** Verify that multi-factor authentication (MFA / 2FA via TOTP or FIDO2/WebAuthn) is supported and enforced on privileged roles.
- [ ] **V2.5.6 (L2):** Verify that account recovery and password reset flows do not disclose whether an account exists (constant-time response and generic messaging).

---

## V3: Session Management Requirements
- [ ] **V3.2.1 (L2):** Verify that session tokens are regenerated after successful authentication to prevent **Session Fixation**.
- [ ] **V3.4.1 (L2):** Verify that session cookies use the `Secure`, `HttpOnly`, and `SameSite=Lax` or `SameSite=Strict` flags.
- [ ] **V3.4.3 (L2):** Verify that session cookies utilize the `__Host-` or `__Secure-` prefixes in production to prevent cookie tossing and subdomain attacks.
- [ ] **V3.5.3 (L2):** Verify that JWT tokens validate the `iss` (issuer), `aud` (audience), `exp` (expiration), and reject `alg: none`.

---

## V4: Access Control Requirements
- [ ] **V4.1.1 (L2):** Verify that access control decisions follow the **Deny by Default** principle: unless explicitly granted, access is blocked.
- [ ] **V4.1.2 (L2):** Verify that authorization checks are performed on the server-side for every single request, never trusting client-side flags.
- [ ] **V4.1.3 (L2):** Verify that access control enforces multi-tenant boundary checks (tenant ownership scoped in DB queries) to eliminate **BOLA / IDOR**.
- [ ] **V4.2.1 (L2):** Verify that administrative features are protected by explicit role-based or attribute-based authorization (anti-BFLA).

---

## V5: Validation, Sanitization and Encoding
- [ ] **V5.1.1 (L2):** Verify that input validation uses an allow-list approach (schemas such as Zod, Pydantic, or Joi) applied at the trust boundary.
- [ ] **V5.1.4 (L2):** Verify that regular expressions are checked against catastrophic backtracking (anti-ReDoS).
- [ ] **V5.2.4 (L2):** Verify that template engines (Handlebars, Jinja2, EJS) strictly escape HTML/JS characters and do not execute untrusted expressions.
- [ ] **V5.3.1 (L2):** Verify that all database queries use parameterized interfaces (ORMs, Prepared Statements) without string concatenation.
- [ ] **V5.5.2 (L2):** Verify that deserialization of untrusted data (pickle, yaml.load, Java deserialization) is avoided or protected by cryptographic signatures.

---

## V8: Data Protection & Privacy
- [ ] **V8.2.1 (L2):** Verify that sensitive data (PII, credentials, payment tokens) is encrypted at rest using AES-GCM-256 or cloud KMS keys.
- [ ] **V8.3.1 (L2):** Verify that sensitive memory allocations (passwords, encryption keys) are cleared (*zeroized*) immediately after use.
- [ ] **V8.3.4 (L2):** Verify that secrets and tokens are not logged in plain text in application logs, query strings, or exception messages.

---

## V12: File and Resources Requirements
- [ ] **V12.1.1 (L2):** Verify that file upload handlers inspect the **Magic Bytes** of the file buffer, rather than trusting the filename or `Content-Type` header.
- [ ] **V12.3.1 (L2):** Verify that file paths received from users are resolved against a safe root directory to prevent **Path Traversal** (`../`).
- [ ] **V12.6.1 (L2):** Verify that outbound HTTP requests (webhooks, URL fetches) enforce strict destination allow-lists to eliminate **SSRF**.

---

## V13: API and Web Service Requirements
- [ ] **V13.1.1 (L2):** Verify that all APIs validate that the requesting identity owns or is explicitly authorized to view the requested resource.
- [ ] **V13.1.4 (L2):** Verify that endpoints accept only defined properties to prevent **Mass Assignment** (e.g., stripping unknown fields).
- [ ] **V13.2.1 (L2):** Verify that APIs do not expose internal object models or sensitive fields in JSON response bodies (**Excessive Data Exposure**).
- [ ] **V13.3.1 (L2):** Verify that GraphQL schemas enforce query depth and complexity limits to prevent resource exhaustion attacks.

---

## V14: Configuration Requirements
- [ ] **V14.1.1 (L2):** Verify that build and development features (debug modes, verbose stack traces, Swagger UI in production) are disabled.
- [ ] **V14.4.1 (L2):** Verify that HTTP responses include standard security headers: `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`, `Referrer-Policy`.
- [ ] **V14.4.4 (L2):** Verify that CORS policies do not use wildcard origins (`*`) when credentials are included.
