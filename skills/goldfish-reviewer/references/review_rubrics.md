# Goldfish Review Rubrics & Quality Standards

This document establishes the evaluation standards for specifications and implementation plans reviewed under the Goldfish Review Protocol (EGM).

---

## 1. Zoom Out Standard (Altitude & Simplicity)

### Core Principle
A design passes if it solves the root problem in the simplest possible way, leverages existing infrastructure and codebase conventions, avoids speculative features (YAGNI), and maintains proper abstraction boundaries without getting bogged down in low-level code implementation details.

### Requirements:
- **Root Problem Focus:** Solves the core architectural problem, not a surface symptom.
- **YAGNI (You Aren't Gonna Need It):** Reject abstractions, message queues, caches, or sharding designed solely for hypothetical future scale.
- **Leverage Existing Code:** Reuses existing modules, middlewares, and utilities in the repository rather than introducing new dependencies.
- **Altitude Control:** High-level sections must focus on architecture, boundaries, and contracts, avoiding loop variables or helper functions.

---

## 2. Comprehension Standard (Self-Containment)

### Core Principle
A proposal passes if a competent engineer (or clean-slate AI agent) who is completely unfamiliar with the project can understand the goals, architecture, and constraints without asking clarifying questions.

### Requirements:
- **Zero Jargon:** Technical terms are defined or standard. Marketing jargon (*"effortless"*, *"seamless"*) is banned.
- **Explicit Assumptions:** All operational assumptions (e.g. database versions, network boundaries, authentication flow) are explicitly listed.
- **Data Flow Diagram:** Clear sequence or flowchart describing how data flows through the system components.

---

## 3. Heilmeier Catechism Standard

To satisfy this standard, the proposal must explicitly answer:
1. **Objectives:** What is being attempted? (No jargon).
2. **State of the Art:** How is it solved today, and what are the limitations?
3. **New Approach:** What is new in this approach, and why will it succeed?
4. **Impact:** Who cares? If successful, what difference does it make?
5. **Risks & Payoffs:** What are the risks (e.g. data loss, latency spikes) and the payoff?
6. **Cost:** What is the cost in compute, memory, database load, and engineering time?
7. **Exams & Metrics:** What are the quantifiable milestones and tests to confirm success?

---

## 4. Implementation Readiness Standard (The Zero-Decision Rule)

### Core Principle
An implementation plan passes if an engineer (or coding agent) can execute the plan and produce the correct changes on the first attempt without guessing, asking questions, or making independent architectural choices.

### The Zero-Decision Rule
The plan must leave **zero design or architectural choices to the implementer**. If the implementer must choose:
- File paths or directory names
- Database schemas or column types
- API endpoints or HTTP status codes
- Dependency versions
- Error-handling strategy or edge case fallback behavior

Then the plan **FAILS** the standard immediately. All such decisions must be pre-determined and documented in the plan.
