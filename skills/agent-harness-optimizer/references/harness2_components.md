# Harness² Component Reference & Surface Specification (Google Research)

This reference outlines the architecture of agent harnessing based on Google Research's **Harness²** ([arXiv:2610.14224](https://arxiv.org/abs/2610.14224)).

---

## 1. What is a Harness?

A **harness** is the complete scaffolding system around a foundation model that enables it to act as an agent:
- System prompts and role definitions
- Guardrails and standing constraints
- Long-term memory and durable facts
- Tool descriptions and guidance
- Skills and progressive workflows
- Subagents and delegation structures
- Deterministic helper scripts
- Tool loop hooks and middleware plugins

**Harnessing** is the process of optimizing this scaffolding while keeping the underlying model weights fixed.

---

## 2. The 8 Components Breakdown

| Component | Scope | Token Impact | Recommended Usage |
|---|---|---|---|
| **1. System Prompt / AGENTS.md** | Global | Always-on (High) | High-level role, core invariants, primary workflow entrypoint. |
| **2. Guardrails** | Global | Always-on (High) | Inviolable security boundaries and safety rules. |
| **3. Long-Term Memory** | Global | Always-on (High) | Durable architectural facts, verified schemas, project dictionary. |
| **4. Tool Guidance** | Global | Always-on (Medium) | Operational guidance for shell, file-editing, and custom tools. |
| **5. Skills** | On-demand | Zero standing cost | Specialized multi-step workflows loaded only when triggered. |
| **6. Subagents** | Delegated | Isolated cost | Bounded tasks where the input is large and the output is concise. |
| **7. Scripts** | Deterministic | Zero model cost | Hand-rolled math, formatting, data parsing, or regex checks. |
| **8. Hooks / Plugins** | Tool Loop | Zero model cost | Pre-tool and post-tool interceptors that block illegal actions or truncate noisy outputs. |

---

## 3. The 3 Invariants That Discard a Harness Proposal

In the Harness² framework, candidate harness modifications are immediately discarded if they violate any of these rules:

1. **Every Skill Needs a Trigger Line:**
   If a skill directory `skills/<name>/SKILL.md` exists, its name MUST appear in the always-on context (`AGENTS.md` or `systemprompt.md`) with a clear trigger statement:
   ```markdown
   When <situation>, load the `<name>` skill.
   ```
2. **Every Script You Name Must Exist:**
   Any script referenced in a skill (`skills/<name>/scripts/<file>.py`) or always-on prompt must physically exist in the repository.
3. **No Unescaped Template Tags in Always-On Text:**
   Doubled braces (`{{` or `{%`) in always-on prompts can break template renderers like Jinja2.

---

## 4. Propose–Probe–Compose Cycle

- **Propose:** The harness editor analyzes failed trajectories and proposes two kinds of changes:
  - *Invariant Edits (INV):* Universal procedural hygiene, verification before completion, defensive parsing.
  - *Domain Edits (DOM):* Context-specific business logic, domain heuristics, schema rules.
- **Probe:** Run candidate harnesses against the current task without ground truth feedback.
- **Compose:** Contrast probe execution traces. Merge changes that produced successful behavioral contrasts, discard speculative additions, and prune obsolete text.
