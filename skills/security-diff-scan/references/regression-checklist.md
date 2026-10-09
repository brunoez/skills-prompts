# PR Security Regression Checklist

Use this checklist during PR diff reviews to spot subtle regressions and vulnerabilities introduced by incremental changes.

---

## 1. Authorization & Tenancy Regressions (BOLA / IDOR)

- [ ] **Query Scope Preservation:** Do all modified database queries include tenant scoping (`where: { id, tenant_id }`)?
- [ ] **Decorator & Middleware Integrity:** Were any authorization decorators (`@Roles('ADMIN')`, `@RequireAuth()`) removed from controller methods?
- [ ] **Session Binding:** Is user identity obtained exclusively from the verified session/token (`req.user.id`) rather than editable query/body parameters?
- [ ] **Object Ownership Verification:** When mutating or deleting records (`UPDATE`, `DELETE`), does the code verify that the target object belongs to the authenticated user's organization?

---

## 2. Input Validation & Mass Assignment Regressions

- [ ] **Strict DTO Parsing:** Do newly created or modified Zod/Pydantic schemas enforce `.strict()` or `.strip()` to reject unexpected attributes?
- [ ] **Privilege Escalation via Body:** Does the payload allow updating sensitive fields (`role`, `is_admin`, `verified`, `plan`)?
- [ ] **Type Coercion Hazards:** Are IDs properly validated as UUIDs/integers rather than accepted as raw untyped strings?

---

## 3. Injection & Dangerous Sinks

- [ ] **Raw SQL / ORM Bypasses:** Were any methods changed to `queryRawUnsafe`, `raw()`, or string concatenation in queries?
- [ ] **Command Execution:** Are inputs passed to `child_process.exec`, `os.system`, or shell commands without strict allow-listing?
- [ ] **SSRF in Outbound Calls:** If the PR adds `fetch()` or HTTP client calls with dynamic URLs, is there an allow-list of schemes and domains, and are private IP ranges (RFC 1918, link-local `169.254.169.254`) blocked?

---

## 4. Secret & Configuration Hardening

- [ ] **Embedded Secrets:** Does the diff contain API keys, test tokens with production formats, private keys, or passwords?
- [ ] **CORS & Cookie Flags:** Did the PR widen CORS origins (`*`) or relax cookie security flags (`httpOnly`, `secure`, `sameSite`)?
- [ ] **Error Verbosity:** Does the new error handling code leak internal stack traces or database schema details in HTTP responses?
