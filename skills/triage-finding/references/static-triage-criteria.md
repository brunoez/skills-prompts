# Static Reachability Triage Criteria

This document details the reachability evaluation rules for third-party alerts, based on **OpenAI Codex Security** (`triage-finding`) and the **OWASP Dependency-Check** architecture.

---

## 1. Reachability Tiers for SCA Alerts

When assessing an advisory (e.g., CVE-2024-XXXX affecting `library-x`):

### Tier 1: Package Absent from Runtime
* The dependency is not present in the runtime lockfile or is confined strictly to dev/test environments.
* **Verdict:** `not_actionable` (Dismiss in scanner as "Development dependency / Not packaged in production").

### Tier 2: Package Present, Method Dead Code
* The dependency is imported, but the specific vulnerable API (e.g., `parseXML()` in a utility library) is never invoked anywhere in production code.
* **Verdict:** `not_actionable` (Dismiss as "Unreachable code path / Function not invoked").

### Tier 3: Method Invoked with Static Constants
* The vulnerable function is called, but its arguments are hardcoded string literals or developer constants (not influenced by external user input).
* **Verdict:** `not_actionable` (Dismiss as "Input source is not user-controllable").

### Tier 4: Method Invoked with User Input
* The vulnerable method is reachable from an HTTP route, message consumer, or CLI argument, and no upstream sanitizer neutralizes the payload.
* **Verdict:** `confirmed` (Promote to immediate engineering fix ticket).

---

## 2. When to Assign `needs_review`

Assign `needs_review` when:
* The codebase uses dynamic calls (`import(variable)`, `getattr(mod, func)`, reflection).
* The project is an open-source library or SDK where downstream callers supply the arguments, and the function is part of the public export surface.
* A runtime environment flag or cloud WAF rule is claimed to mitigate the issue, but configuration cannot be statically verified.
