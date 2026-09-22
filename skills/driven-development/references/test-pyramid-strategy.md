# The Test Pyramid & Multi-Tier Automation Strategy

The **Test Pyramid** ensures that the automated test suite provides maximum confidence, fast feedback loops, and resilient continuous integration.

---

## 1. Test Pyramid Tiers

```plaintext
      / \
     / E2E \         (10%) Playwright / Cypress — Critical User Journeys
    /-------\
   / Integr. \       (20%) Testcontainers / Supertest — Real DB, Cache & APIs
  /-----------\
 /  Unit Tests \     (70%) Vitest / Pytest — Pure Domain Logic, Schemas, State Machines
/---------------\
```

### 1. Unit Tests (70%)
* **Scope:** Individual functions, domain entities, value objects, schema validators, state transitions.
* **Execution Time:** Under 10ms per test. Zero external I/O.
* **Tooling:** Vitest, Jest, Pytest, Go test, Cargo test.

### 2. Integration Tests (20%)
* **Scope:** HTTP controllers, database repositories, message broker publishers, middleware chains.
* **Execution Time:** 50ms - 500ms per test.
* **Tooling:** Supertest, Testcontainers (PostgreSQL, Redis, RabbitMQ), FastAPI TestClient.

### 3. End-to-End (E2E) Tests (10%)
* **Scope:** Complete end-to-end user workflows from frontend UI to database persistence.
* **Execution Time:** 1s - 5s per test.
* **Tooling:** Playwright, Cypress.

### 4. Load & Performance Testing (Ad-hoc / Nightly)
* **Scope:** Throughput, concurrency bottlenecks, connection pool starvation.
* **Tooling:** k6, Locust, Artillery.

---

## 2. Invariants Over Coverage Metrics

* **The Vanity Trap:** 100% line coverage does not guarantee quality if tests lack meaningful assertions.
* **The Invariant Standard:** Every test must assert an architectural or business invariant:
  1. No state corruption.
  2. Strict boundary enforcement.
  3. Correct error signaling under unexpected inputs.
