---
name: appsec-auditor
description: Use when auditing codebases, APIs, controllers, or database queries for vulnerabilities, OWASP Top 10, ASVS compliance, BOLA/IDOR, SQLi, SSRF, broken authentication, or when generating SARIF/PDF security audit reports.
---

# AppSec Auditor (OWASP ASTF, ASVS v4.0.3 & Risk Rating)

This skill equips the agent to perform enterprise-grade Application Security audits across web applications, REST/GraphQL/gRPC APIs, database access layers, and cloud integrations.

It applies the **OWASP API Security Testing Framework (ASTF)**, normative criteria from **OWASP ASVS v4.0.3 (Level 2)**, and calculates risk deterministically using the **OWASP Risk Rating Methodology** (Likelihood $\times$ Impact).

---

## When to Use

Use this skill whenever:
* The user asks to audit the security of an API, controller, route handler, or backend repository.
* Verifying code against **OWASP Top 10**, **OWASP API Top 10 2023**, or **OWASP ASVS**.
* Investigating access control vulnerabilities (**BOLA / IDOR / BFLA**), multi-tenant data leakage, or Mass Assignment.
* Auditing outbound requests for **Server-Side Request Forgery (SSRF)** or DNS rebinding.
* Reviewing authentication, password hashing (**Argon2id**), JWT signing, or session fixation risks.
* Generating compliant **SARIF 2.1.0** reports for GitHub Code Scanning / GitLab Security or executive PDF/Markdown reports.

## When NOT to Use

* For pre-implementation architecture threat modeling before code exists (use `threat-modeler` or `prompts/security/threat_modeling.md`).
* For pure unit test creation without security abuse testing (use `driven-development`).
* For fast System 1 runtime guardrails or prompt screening (use `jev-system-one`).

---

## 5-Phase Audit Workflow (Mantis-Enhanced)

```mermaid
flowchart LR
    P1["Phase 1:<br/>Surface Discovery"] --> P2["Phase 2:<br/>Deep Code Audit"]
    P2 --> P3["Phase 3:<br/>Viability Critique"]
    P3 --> P4["Phase 4:<br/>Calibrated Rating"]
    P4 --> P5["Phase 5:<br/>PoC & Artifact Gen"]
```

### Phase 1: Attack Surface Discovery & Contract Mapping
1. **Map Entry Points:** Scan routers, controllers, handlers, GraphQL schemas, and gRPC definitions.
2. **Contract Comparison:** Compare OpenAPI/Swagger specs with live controllers to detect **Shadow/Zombie APIs** (ASVS V13.2.2).
3. **Identify Trust Boundaries:** Mark unauthenticated public endpoints vs authenticated multi-tenant routes.

### Phase 2: Systematic Code Inspection (Zero Speculative Assumptions)
Audit each file line by line against the core vulnerability vectors. Consult the modular references:
* [OWASP ASTF & API Top 10 Guide](references/owasp-api-astf.md)
* [ASVS v4.0.3 Verification Checklist](references/asvs-v4-checklist.md)
* [Access Control & BOLA Deep Dive](references/access-control-bola.md)
* [SSRF Prevention & Safe Egress](references/ssrf-prevention.md)

### Phase 3: Viability Critique & Anti-Hallucination (Google Mantis Inspired)
Eliminate false positives and verify release-build viability using [Viability Critique](references/viability-critique.md):
1. **Reachability Check:** Confirm the vulnerable path is actively routed and reachable from external inputs (eliminate dead code).
2. **Release Viability:** Discard `assert`-only issues that disappear in release/production builds (`python -O`, bundled production).
3. **Upstream Neutralization:** Verify if reverse proxies, WAFs, or global DTO validation pipes already strip or sanitize the input.

### Phase 4: Deterministic OWASP Risk Rating & Calibrated Scoring
Calculate the practical risk using the [Risk Rating & Mantis Calibration](references/risk-rating-methodology.md):

$$\text{Calibrated Score (1-10)} = \text{Base Severity} \times M_{\text{evidence}} \times M_{\text{viability}}$$

* **9.0 a 10.0** = 🔴 **CRÍTICA** (RCE, public unauthenticated BOLA, proved by PoC or visible without sanitizer).
* **7.0 a 8.9** = 🟠 **ALTA** (Cross-tenant IDOR, missing tenancy filter in update).
* **4.0 a 6.9** = 🟡 **MÉDIA** (Stored XSS requiring admin view, missing rate limit).
* **1.0 a 3.9** = 🔵 **BAIXA / INFO** (Verbose technical banner, missing non-critical header).

### Phase 5: PoC Reproduction, Remediation & Artifact Generation
1. **PoC Micro-Harness:** Structure reproducible test cases following [PoC Reproduction Harness](references/poc-reproduction-harness.md) (Tier 1 unit test, Tier 2 functional mock, or Tier 3 sandbox).
2. **Terminal Prioritization Table:** Present a quick-wins summary table.
3. **Defensive Code Fixes:** Provide drop-in patches implementing defense-in-depth.
4. **SARIF 2.1.0 & Markdown Export:** Execute `sarif_builder.py` and `report_generator.py`.

---

## Executable Tools & Scripts in this Skill

### 1. Generating SARIF 2.1.0 for GitHub / CI/CD
The skill includes `scripts/sarif_builder.py` to create standards-compliant SARIF output from findings:

```bash
python3 skills/appsec-auditor/scripts/sarif_builder.py \
  --input findings.json \
  --output results.sarif
```

### 2. Generating Markdown Executive Reports & Issue Templates
The skill includes `scripts/report_generator.py` to produce full audit documentation:

```bash
python3 skills/appsec-auditor/scripts/report_generator.py \
  --input findings.json \
  --output docs/security-audit-report.md \
  --issues-dir docs/issues/
```

### Format of `findings.json`:
```json
[
  {
    "id": "SEC-001",
    "title": "BOLA in Invoice Retrieval Endpoint",
    "description": "Endpoint /api/invoices/:id queries DB by primary key without checking organizationId.",
    "severity": "CRITICAL",
    "file_path": "src/controllers/invoice.controller.ts",
    "start_line": 42,
    "end_line": 48,
    "owasp": "API1:2023",
    "asvs": "V13.1.1",
    "cwe": "CWE-639",
    "likelihood": "Alta",
    "impact": "Alto",
    "risk_score": 9.5,
    "viability": "RELEASE_EXPLOITABLE",
    "poc_tier": "TIER_1_UNIT",
    "effort": "Baixo",
    "quick_win": true,
    "remediation": "Enforce req.user.organizationId in prisma query.",
    "verification": "pytest tests/test_bola.py"
  }
]
```

---

## Verified Code References & Examples
* [Viability Critique & Anti-Hallucination](references/viability-critique.md): Filter rules for release builds and dead code.
* [PoC Reproduction Harness](references/poc-reproduction-harness.md): 3-tier reproduction strategy and templates.
* [Automated BOLA Abuse Test Example](examples/bola_idor_test.py): Real pytest test case testing cross-tenant isolation.
* [SSRF-Safe Fetch Client](examples/ssrf_safe_fetch.ts): TypeScript client with pre-flight DNS check and IP pinning.

