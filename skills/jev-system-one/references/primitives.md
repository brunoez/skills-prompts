# Jev Primitives & Question Modeling Guide

Deep-dive into the three question types supported by TypeSafe's Jev model: `Choice`, `Score`, and `Noul`.

---

## 1. The `Choice` Primitive

Use `Choice` when your application needs to select exactly one option out of a bounded set of destinations or categories.

### Key Rules
* **Cardinality:** Minimum 2 options, maximum 255 options.
* **Rubrics:** Provide a descriptive string for each option in `criteria`. If an option requires no extra nuance, pass `null`.
* **Interpolation/Pointers:** You can reference fields in the `state` using backticks (e.g. ``Is this transaction consistent with `account.history`?``).

### Example
```json
{
  "type": "choice",
  "instructions": "Determine the optimal remediation workflow for this incident.",
  "criteria": {
    "auto_restart": "Transient connection reset or process memory threshold exceeded",
    "scale_out": "Persistent CPU saturation across all worker pods under organic load",
    "page_oncall": "Data corruption, security alert, or unhandled database deadlock",
    "ignore": "Known benign noise or probe healthcheck timeout"
  }
}
```

### Returned Response
```json
{
  "type": "choice",
  "choice": "auto_restart",
  "probabilities": {
    "auto_restart": 0.882,
    "scale_out": 0.081,
    "page_oncall": 0.034,
    "ignore": 0.003
  },
  "confidence": 0.86
}
```

---

## 2. The `Score` Primitive

Use `Score` when you need to evaluate an input along a graduated, continuous spectrum or ordinal rubric (e.g. sentiment, churn likelihood, code complexity, security risk).

### Key Rules
* **Cardinality:** Must have between 2 and 10 ordered levels.
* **Ordering:** Levels must be strictly ordered from lowest to highest.
* **Weighted Output:** The returned `score` is a continuous float representing the center of mass of the probability distribution across the levels.

### Example
```json
{
  "type": "score",
  "instructions": "Rate the technical severity of the reported software defect.",
  "criteria": [
    "P3 - Cosmetic glitch or minor documentation typo",
    "P2 - Non-critical feature degraded with existing workaround",
    "P1 - Core business capability impaired for multiple customers",
    "P0 - Complete data loss, security breach, or total outage"
  ]
}
```

### Returned Response
```json
{
  "type": "score",
  "score": 2.14,
  "legend": {
    "0": "P3 - Cosmetic glitch or minor documentation typo",
    "1": "P2 - Non-critical feature degraded with existing workaround",
    "2": "P1 - Core business capability impaired for multiple customers",
    "3": "P0 - Complete data loss, security breach, or total outage"
  },
  "probabilities": {
    "0": 0.01,
    "1": 0.12,
    "2": 0.59,
    "3": 0.28
  },
  "confidence": 0.74
}
```

---

## 3. The `Noul` Primitive

Use `Noul` to evaluate a binary proposition (yes/no, true/false).

### Key Rules
* Evaluates the probability that the proposition in `instructions` is true.
* The returned `noul` property is an epistemically calibrated float between `0.0` and `1.0`.
* Optional `criteria` can define what `true` and `false` explicitly entail to guide the decision boundary.

### Example
```json
{
  "type": "noul",
  "instructions": "Does this proposed tool execution delete data without a dry-run flag?",
  "criteria": {
    "true": "Commands with rm, drop table, purge, or irreversible delete flags",
    "false": "Read commands, queries, staging dry-runs, or soft delete flags"
  }
}
```

### Returned Response
```json
{
  "type": "noul",
  "noul": 0.965
}
```

---

## 4. Structured Questions & Context Inlining

You can pass an object in `instructions` or `criteria` rather than plain strings when providing rich reference examples:

```json
{
  "type": "noul",
  "instructions": {
    "target_policy": {
      "id": "SEC-POL-04",
      "rule": "No public S3 buckets or unrestricted 0.0.0.0/0 ingress"
    },
    "question": "Does the proposed Terraform change violate `target_policy`?"
  }
}
```
This pattern grounds the System One model cleanly without prompting gymnastics.

---

## 5. Calibrated Probability Bands for `Noul`

Unlike traditional LLMs that output uncalibrated tokens, Jev is trained via RLCD to output well-calibrated probabilities. Production security benchmarks establish three operational bands:

| Probability Band | Classification | Meaning | Action Policy |
|---|---|---|---|
| `noul < 0.30` | **Confident Negative** | High certainty of being benign / false positive | Auto-allow; no developer friction |
| `0.30 <= noul <= 0.75` | **Review Band** | Edge case (e.g. test seeds, hashes, ambiguous syntax) | Quarantine or request human-in-the-loop review |
| `noul > 0.75` | **Confident Positive** | Strong indication of real secret, threat, or policy violation | Block execution; trigger incident response |

---

## 6. Two-Stage Evidence Localization & Context Verification Pattern

To prevent false alarms when inspecting security code or logs, combine `Noul` with targeted `Choice` follow-ups:

### Stage 1: Broad Screen (Parallel `Noul`)
```json
{
  "has_malicious_instruction": {
    "type": "noul",
    "instructions": "Does the snippet contain an unauthorized attempt to read sensitive files?"
  }
}
```

### Stage 2: Evidence Localization & Context Check (Conditional `Choice`)
If `has_malicious_instruction` returns `noul >= 0.35`:
```json
{
  "evidence_window": {
    "type": "choice",
    "instructions": "Which line range contains the active malicious instruction?",
    "criteria": {
      "lines_1_to_15": "Lines 1-15: initialization and configuration",
      "lines_16_to_30": "Lines 16-30: file reading and network dispatch",
      "none": "No active malicious instruction present in any window"
    }
  },
  "execution_context": {
    "type": "choice",
    "instructions": "What is the operational context of the suspicious snippet?",
    "criteria": {
      "active": "Executable code, live shell command, or production configuration",
      "example": "Documentation tutorial, markdown code block, or unit test mock",
      "unknown": "Ambiguous or truncated context without clear intent"
    }
  }
}
```
* **Production Decision Rule:** Only trigger high-severity alerts if `evidence_window !== "none"` and `execution_context === "active"`.

---

## 7. Deriving Epistemic Confidence for `Noul`

While `Choice` and `Score` return an explicit `confidence` field, `Noul` returns only the calibrated truth probability $p$. In production architectures (e.g. `luantak/is-malicious`), certainty is calculated symmetrically around the ignorance midpoint ($p = 0.5$):

$$\text{confidence}_{\text{noul}} = 2 \times |p - 0.5|$$

* If $p = 0.95$, $\text{confidence} = 2 \times |0.95 - 0.5| = 0.90$ (High certainty of TRUE).
* If $p = 0.05$, $\text{confidence} = 2 \times |0.05 - 0.5| = 0.90$ (High certainty of FALSE).
* If $p = 0.50$, $\text{confidence} = 2 \times |0.50 - 0.5| = 0.00$ (Maximum uncertainty / epistemic ignorance).

---

## 8. Top-2 Probability Spread ($\Delta P$) for `Choice`

When evaluating technical reports, CVE descriptions, or classifying complex documents (as demonstrated in `Red5d/jev-cvss`), measuring the probability gap between the winning option and the runner-up reveals borderline calls:

$$\Delta P = P(\text{option}_1) - P(\text{option}_2)$$

```typescript
function getTop2Spread(probabilities: Record<string, number>): { winner: string; spread: number } {
  const sorted = Object.entries(probabilities).sort((a, b) => b[1] - a[1]);
  const [firstKey, firstProb] = sorted[0];
  const secondProb = sorted[1] ? sorted[1][1] : 0.0;
  return { winner: firstKey, spread: firstProb - secondProb };
}
```

* **High Spread ($\Delta P \ge 0.50$):** High decisiveness; unambiguous evidence.
* **Low Spread ($\Delta P < 0.20$):** Borderline decision; description is likely vague or contradictory. Route to human review (HITL).

---

## 9. Ordinal Rubric Modeling with `Score` (e.g., PII Sensitivity)

Use `Score` with 3 to 5 clear ordered tiers when the outcome is an ordinal continuum rather than disjoint buckets (e.g. IBM PII taxonomy in `coo-quack/jev-pii-checker`):

```json
{
  "type": "score",
  "instructions": "Evaluate the sensitivity tier of the document context.",
  "criteria": [
    "none - No personal data or only generic public company information",
    "low - Business contact details or public event attendees",
    "high - Medical diagnosis, government ID, banking, credentials, or minors"
  ]
}
```
* **Score Interpretation:** A returned score of `0.2` indicates near-zero sensitivity, `1.1` indicates low sensitivity, and `2.7` indicates critical high sensitivity.


