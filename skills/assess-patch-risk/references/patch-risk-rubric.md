# Patch Risk Rubric & Auto-Merge Evaluation Guide

This document defines the normative rubric for evaluating patch artifacts, based on the **OpenAI Codex Security** `assess-patch-risk` contract and Google SRE release engineering principles.

---

## 1. The Strict Auto-Merge Gates

To receive the `auto_merge_candidate` label, a patch MUST pass all of the following gates without exception:

### Gate 1: Zero Schema & Persistence Mutations
* ❌ Modifies SQL migrations (`migrations/`, `*.sql`), Prisma schemas, TypeORM entities, or alembic scripts.
* ❌ Adds new database tables, columns, indexes, or modifies constraints.
* 👉 *Reason: Schema migrations require coordinated rollback strategies and cannot be safely merged by autonomous agents without human signoff.*

### Gate 2: Zero Public Contract Changes
* ❌ Alters parameter types, names, or order in public library APIs or REST/GraphQL endpoints.
* ❌ Modifies HTTP response status codes (e.g., changing 200 OK to 404 Not Found on an existing route).
* ❌ Removes or renames JSON response fields.

### Gate 3: Bundled Regression Protection
* ✅ Patch includes at least one automated test verifying that the target issue is fixed.
* ✅ Patch includes test coverage demonstrating that valid, existing user inputs continue to be accepted.

### Gate 4: Blast Radius & Reversibility
* ✅ The patch modifies only leaf-level functions or private helpers.
* ✅ Reversion via `git revert` is completely clean and introduces zero residual state corruption.

---

## 2. When to Assign `human_review_required`

Assign `human_review_required` when the patch is technically sound, but involves:
* Authentication, session management, or cryptography routines (`auth`, `jwt`, `argon2`, `crypto`).
* Billing, payments, pricing, or checkout workflows.
* Environment configuration, secrets management, or deployment scripts (`Dockerfile`, CI/CD workflows).
* Database queries modifying multi-tenant indexing or tenant separation.

---

## 3. When to Assign `revise` or `block`

* **`revise`:**
  - The patch fixes the vulnerability for the exact payload reported, but misses trivial bypasses (e.g., handles lowercase URL encoding but fails on uppercase).
  - The patch lacks automated tests.
  - The patch introduces potential performance regressions (e.g., unindexed query in a hot loop).
* **`block`:**
  - The patch breaks existing unit tests.
  - The patch weakens security (e.g., bypasses an authorization check to "fix" an access issue).
  - The patch introduces breaking syntax, unimported modules, or fails linting.
