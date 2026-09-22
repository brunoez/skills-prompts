# OWASP Risk Rating Methodology & Severity Matrix

The **OWASP Risk Rating Methodology** establishes a standardized, reproducible formula for calculating the practical risk of identified security vulnerabilities.

$$\text{Risk (Severity)} = \text{Likelihood} \times \text{Impact}$$

---

## 1. Calculating Likelihood (Probabilidade)

Likelihood measures how probable it is that a vulnerability will be discovered and actively exploited.

| Level | Criteria & Exploitability | Typical Scenarios |
| :--- | :--- | :--- |
| **ALTA (High)** | Exploitable without authentication, readily discoverable, no specialized tools needed, public automated scanners cover this. | Unauthenticated BOLA with sequential IDs, reflected XSS, public secrets in git, missing auth on admin route. |
| **MÉDIA (Medium)** | Requires authenticated user account, specific timing, non-obvious parameter manipulation, or multi-step execution. | Cross-tenant IDOR between authenticated users, mass assignment on secondary update route, stored XSS requiring admin view. |
| **BAIXA (Low)** | Requires privileged insider access, complex preconditions, race conditions with microsecond windows, or obscure local configuration. | Local file write requiring existing arbitrary file read, theoretical timing side-channel on non-critical hash. |

---

## 2. Calculating Impact (Impacto)

Impact measures the damage caused to technical systems, business operations, and customer data if exploitation succeeds.

| Level | Criteria & Blast Radius | Typical Scenarios |
| :--- | :--- | :--- |
| **ALTO (High)** | Total compromise of data confidentiality, integrity, or availability. Remote Code Execution (RCE), full database dump, account takeover (ATO), or complete financial theft. | SQL Injection, SSRF to cloud metadata, hardcoded production database root password, zeroization failure on private keys. |
| **MÉDIO (Medium)** | Unauthorized access to limited records, partial denial of service, elevation of user privileges within a single tenant, or exposure of non-critical PII. | Information leakage of non-sensitive analytics, localized rate limit bypass, bypass of non-critical business flow. |
| **BAIXO (Low)** | Minimal technical impact, no data leakage, slight inconvenience, or exposure of verbose system headers without exploitable state. | Missing non-critical HTTP header (`Referrer-Policy`), verbose error message without secrets, lack of autocomplete attribute. |

---

## 3. The 3x3 Deterministic Risk Matrix

| Likelihood \ Impact | **BAIXO (Low)** | **MÉDIO (Medium)** | **ALTO (High)** |
| :---: | :---: | :---: | :---: |
| **ALTA (High)** | 🟡 MÉDIA | 🟠 ALTA | 🔴 **CRÍTICA** |
| **MÉDIA (Medium)** | 🔵 BAIXA | 🟡 MÉDIA | 🟠 ALTA |
| **BAIXA (Low)** | 🔵 BAIXA | 🔵 BAIXA | 🟡 MÉDIA |

---

## 4. Blast Radius vs. Theoretical Fatigue

To prevent **alert fatigue**, auditors must distinguish between theoretical concerns and actual blast radius:

1. **Verify Live Code Execution:** Check if the vulnerable code path is actually reachable from public or authenticated entry points.
2. **Look for Defense-in-Depth:** Check if an upstream firewall, API gateway, or TypeScript compiler enforces invariants that neutralize the theoretical risk.
3. **Tag Minor Improvements as `[NIT]`:** Code style or defense-in-depth suggestions that do not represent an exploitable flaw should be classified as `[NIT]` so they do not block deployment or pollute SARIF scanners.
