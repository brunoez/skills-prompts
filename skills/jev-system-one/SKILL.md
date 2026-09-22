---
name: jev-system-one
description: Expert guidance, architectural patterns, and primitives for integrating TypeSafe AI's Jev (System One model) into codebases, agent loops, guardrails, and data pipelines. Use when designing fast decision workflows, model routing, agent tool-call screening, or evaluating structured state with Choice, Score, and Noul primitives.
---

# Jev & System One Decision Models (TypeSafe AI)

This skill provides comprehensive instructions, patterns, and architectural guardrails for building software and AI agent systems using **Jev**, the flagship **System One Model** from **TypeSafe AI**.

## What is a System One Model?

A System One model is an AI model class engineered specifically for **machine-native automation and software decision-making**, rather than human-oriented text generation.

* **Input:** Structured program state (text string, JSON object, or array of strings) + a map of typed questions.
* **Output:** Strongly-typed answers (`Choice`, `Score`, `Noul`) with calibrated probability distributions and confidence scores.
* **Core Differences vs. Traditional LLMs:**
  * **No string/chat generation:** It does not produce conversational prose, explanations, or code.
  * **Zero Type Errors & Zero Hallucination:** The answer space is bound to the schema provided in the request. Mathematical guarantee of schema conformance.
  * **Parallel Sampling:** All questions in a request are evaluated concurrently in a single forward pass (~70ms to 500ms).
  * **Calibrated Probabilities (RLCD):** Trained via *Reinforcement Learning for Calibrated Decisions* on synthetic data so that probabilities reflect empirical reality.
  * **Cost Efficiency:** $0.042 / MTok input ($42 / BTok); output tokens are free.

---

## When to Use Jev (High-Value Fits)

Use Jev whenever a software workflow requires a fast, repeatable, structured decision on an unstructured or semi-structured state:

1. **Agent Tool Guardrails & Auto-Mode:** Screening tool calls (e.g. bash commands, SQL migrations, destructive file operations) in <100ms before execution to block prompt injection or excessive agency.
2. **Intent Routing & Dynamic Dispatch:** Categorizing incoming requests, events, or tickets and routing them to deterministic code, cheap models, or deep reasoning models.
3. **Speculative Fan-out:** Asking 5 to 20 independent classification, triage, and scoring questions about a single state in one parallel call without increasing latency.
4. **Content & Event Triage:** Filtering spam, detecting customer churn signals, calculating lead priority, and labeling real-time feeds at high throughput.
5. **RAG Citation & Faithfulness Verification:** Verifying whether a generated claim is supported by a retrieved source excerpt without running an expensive second LLM-as-a-judge.

---

## When NOT to Use Jev (Anti-Patterns & Overkill)

Avoid using Jev for:
* **Text or Code Generation:** Writing essays, drafting conversational responses, summarizing documents, or writing functions. (Use System 2 LLMs).
* **Pure Arithmetic or Numeric Math:** Calculating sums, financial compound interest, or statistical metrics. (Keep math in deterministic code).
* **Date & Timestamp Math:** Calculating elapsed business days or timezone conversions. (Parse with code, use Jev only for semantic date extraction).
* **Massive Unpruned Contexts (> 64,000 tokens):** Jev's context window is 64k tokens. Pre-filter your state to include only relevant context.

---

## The Three Core Primitives

All Jev evaluations consist of one or more of these three question types:

### 1. `Choice` (Discrete Categorization)
Selects exactly one option from a set you define (up to 255 options).
* **Question Schema:**
  ```json
  "department": {
    "type": "choice",
    "instructions": "Which department should handle this customer inquiry?",
    "criteria": {
      "billing": "Invoices, payment failures, refunds, subscription plans",
      "technical": "API errors, latency, bugs, system outages",
      "sales": "Custom enterprise pricing, contracts, demo requests"
    }
  }
  ```
* **Answer Returned:** `choice` (string key), `probabilities` (map of float summing to 1.0), `confidence` (float 0.0 to 1.0).

### 2. `Score` (Ordinal Metric / Rubric)
Rates the state along an ordered rubric of 2 to 10 levels. Returns a continuous probability-weighted value.
* **Question Schema:**
  ```json
  "urgency": {
    "type": "score",
    "instructions": "Rate the customer's perceived operational urgency.",
    "criteria": ["Low / Routine", "Moderate / Inconvenient", "Critical / Outage"]
  }
  ```
* **Answer Returned:** `score` (float interpolated across levels), `legend` (map index -> string), `probabilities` (map index -> float), `confidence` (float 0.0 to 1.0).

### 3. `Noul` (Boolean Truth Probability)
Evaluates a specific yes/no proposition and returns the calibrated probability that it is true.
* **Question Schema:**
  ```json
  "is_destructive": {
    "type": "noul",
    "instructions": "Does the command permanently delete or alter production data?",
    "criteria": {
      "true": "Commands like rm, drop, truncate, or bulk delete",
      "false": "Read-only commands, queries, or benign status checks"
    }
  }
  ```
* **Answer Returned:** `noul` (float from 0.0 to 1.0).

---

## Confidence-Gated Architecture

Always distinguish between **Probability** and **Confidence**:
* **Probability:** Distribution over outcomes.
* **Confidence:** Concentration of certainty (entropy metric).

### Safe Production Flow:
```typescript
const result = await typesafe.evaluate({ state, questions });
const answer = result.answers.risk_assessment;

if (answer.confidence >= 0.85) {
  // Safe to act autonomously
  if (answer.choice === "safe") await executeAction();
  else await blockAction();
} else if (answer.confidence >= 0.60) {
  // Ambiguous: Fallback to conservative action or gather more context
  await collectAdditionalContext();
} else {
  // Low confidence ("I don't know"): Escalate to Human-in-the-Loop or frontier reasoning LLM
  await routeToHumanReview();
}
```

---

## Detailed References and Examples in this Skill

Consult the accompanying files for exact implementation details:
* [API Reference](references/api-reference.md): Complete HTTP contract, endpoints, headers, error codes, connection pooling, and concurrency engineering.
* [Primitives Guide](references/primitives.md): In-depth specs for Choice, Score, Noul, calibrated probability bands, and two-stage localization.
* [Anti-Patterns & Jaggedness](references/anti-patterns-jaggedness.md): Known edge cases of Jev 1.13, config-shaped secret triage, and architectural anti-patterns.
* [Two-Model Cascade Example](examples/two-model-cascade.ts): Production TypeScript pattern combining Jev + frontier LLM.
* [LangChain Agent Guardrail](examples/agent-guardrail-langchain.py): Production Python agent interceptor with `AutoModeMiddleware`.
* [Hybrid Secret Detection Pipeline](examples/secret-detection-hybrid.py): Production Python scanner combining regex with Jev Noul semantic validation.
* [Agent Skill & MCP Auditor](examples/mcp-security-auditor.py): Multi-stage auditor for `SKILL.md` prompt injection and MCP tool poisoning.
* [Three-Layer PII Sanitizer Guardrail](examples/pii-sanitizer-guardrail.py): PII detection, IBM sensitivity scoring, digit disambiguation, and masking.
* [Deterministic CVSS v3.1 Metric Calculator](examples/cvss-metric-calculator.py): Parallel Choice metric elicitation with official closed-form FIRST calculation.


