# Jev 1.13 Jaggedness & Anti-Patterns Reference

Guidelines on avoiding failure modes and known jagged edges when deploying Jev in software architectures.

---

## 1. Summary of Known Jagged Edges (Jev 1.13)

| Jagged Edge | Symptom / Risk | Correct Architectural Alternative |
|---|---|---|
| **Literal Reading** | Jev interprets instructions verbatim without extrapolating common business assumptions | Explicitly spell out criteria in each option of `Choice` or `Score` |
| **Arithmetic & Math** | Inaccurate results when asked to calculate sums, percentages, or differences | Keep math in deterministic code; use Jev only to extract categories |
| **Date & Time Comparisons** | Fails on temporal calculations (e.g. "Was this filed within 30 days of invoice date?") | Extract dates with Jev or regex; compare timestamps in application code |
| **Multi-Hop Indirection** | Performance drops when answering questions requiring multi-layered reasoning chains | Decompose into multiple simple questions evaluated in parallel |
| **Bloated State (>64k tokens)** | Exceeds context window or dilutes attention across irrelevant text | Pre-filter or slice state to contain only relevant evidence |
| **Adversarial Input** | Malicious user input attempting to skew probabilities | Apply strict validation, sanitation, and confidence thresholds |

---

## 2. Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Asking Jev to Generate Explanations
* **Insecure / Broken Pattern:** Trying to ask Jev to explain why it chose an option.
* **Why it fails:** Jev does not have a text generator. It returns only schemas and numbers.
* **Fix:** If explanations are required for the user, use the Two-Model Cascade: Jev selects the decision fast, and if necessary, a small LLM drafts the human-readable explanation based on the chosen category.

### ❌ Anti-Pattern 2: Hardcoding Global Confidence Thresholds
* **Broken Pattern:** Using `confidence >= 0.80` for every action in the company.
* **Why it fails:** Risk is asymmetric. A false positive on marketing email tagging is harmless ($0 cost); a false positive on `DROP DATABASE` or automated wire transfer is catastrophic.
* **Fix:** Scale confidence thresholds to business impact:
  * Low impact (read-only, tagging, cache routing): `confidence >= 0.70`
  * Medium impact (customer notifications, ticket routing): `confidence >= 0.85`
  * High impact (data deletion, financial operations, privilege escalation): `confidence >= 0.98` + mandatory human approval.

### ❌ Anti-Pattern 3: Sending Monolithic Free-form Prompts
* **Broken Pattern:** Dumping 5 pages of documentation and asking: *"What should I do?"*
* **Why it fails:** System One models thrive on snap judgments with clear schemas.
* **Fix:** Break the decision into discrete facets:
  1. What type of request is this? (`Choice`)
  2. What is the severity? (`Score`)
  3. Does it require escalation? (`Noul`)

### ❌ Anti-Pattern 4: Failing Builds on Ambiguous Review Band (0.30 - 0.75)
* **Empirical Finding (from `jev-secret-detection`):** Real-world password hashes (SCRAM verifiers, `.htpasswd` apr1/bcrypt digests) and standard mock test seeds (`changeit`, `hunter2`, `correct horse battery staple`) score between `0.50` and `0.73`. They are not true leaks, but look structurally like credentials.
* **Fix:** Never fail automated CI/CD builds or trigger incident alarms on scores between `0.30` and `0.75`. Route these to a secondary triage queue or request developer confirmation in pull requests. Reserve hard blocking for `noul > 0.75`.

### ❌ Anti-Pattern 5: Stripping Resource Context (Asset Pairing)
* **Empirical Finding:** Low-entropy secrets without explicit field names (e.g., SNMP read strings, raw connection tokens) score lower (~0.40 - 0.45) if isolated as lone strings.
* **Fix:** Always keep the adjacent configuration context (database URI, endpoint hostname, or service block) in the snippet sent to Jev. Context enables Jev to recognize operational semantic role.

### ❌ Anti-Pattern 6: Ignoring Execution Context in Security Scanning
* **Empirical Finding (from `jev-security-scan`):** Scanning Markdown docs or security research repos will flag exploit examples as high-risk unless the execution context is evaluated.
* **Fix:** Always pair threat identification with a context classifier `Choice` (`active` vs `example` vs `unknown`), and only alert on active execution context.

### ❌ Anti-Pattern 7: Unbounded Concurrency Flooding
* **Empirical Finding:** Sending 100+ requests simultaneously triggers HTTP `529 Overloaded` and pushes latency past 2 seconds.
* **Fix:** Use an asynchronous semaphore limited to `16` concurrent requests with exponential backoff on 429/529.

### ❌ Anti-Pattern 8: Computing Numeric Scores (CVSS, Math) Inside the Model
* **Broken Pattern:** Asking Jev or an LLM to output a float score like `"7.5"` or `"9.8"` directly for a vulnerability description.
* **Why it fails:** Neural models hallucinate floating-point arithmetic, miscalculate weights (e.g. Scope Changed multipliers), and botch rounding specifications.
* **Fix (from `Red5d/jev-cvss`):** Elicit only categorical metric choices (`AV`, `AC`, `PR`, `UI`, `S`, `C`, `I`, `A`) from Jev. Compute the exact closed-form FIRST math and MacroVectors in deterministic Python/TypeScript code.

### ❌ Anti-Pattern 9: Exposing Jev API Keys to Fork PRs (`pull_request_target`)
* **Security Risk (from `luantak/is-malicious`):** Running CI scans on GitHub fork PRs by switching workflows to `pull_request_target` to pass `TYPESAFE_API_KEY`.
* **Why it fails:** Untrusted code in a fork PR can hijack the GitHub Actions runner and exfiltrate secrets or burn quota.
* **Fix:** Use separate workflows: run read-only local static checks on fork PRs, or trigger Jev scans only upon manual staff approval / comments (`scan-pr-comment.yml`).

### ❌ Anti-Pattern 10: Static Chunking Without `max_tokens_exceeded` Recovery
* **Broken Pattern:** Slicing files by fixed line count without handling token overflows.
* **Why it fails:** Minified JS, binary base64, or dense configs exceed token limits, causing 422 or 400 errors.
* **Fix:** When Jev returns `max_tokens_exceeded`, recursively split the chunk in half and evaluate sub-chunks.


