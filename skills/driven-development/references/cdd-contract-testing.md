# Contract-Driven Development (CDD) & Consumer-Driven Contracts

**Contract-Driven Development (CDD)** guarantees that microservices, third-party clients, and frontend SPAs interact through strict, versioned, and machine-validated contracts (**OpenAPI**, **AsyncAPI**, **Pact**), preventing breaking changes in production.

---

## 1. OpenAPI & Schema Drift Prevention

1. **Contract Ingestion:** Every API endpoint must have a corresponding schema in `openapi.yaml`.
2. **Automated Drift Verification:** Validate that controllers do not return unadvertised fields or omit required fields:
   ```bash
   # Validate OpenAPI schema conformance
   npx @redocly/cli lint openapi.yaml
   ```
3. **Additive-Only Evolutions:**
   - Field additions must always be optional/defaulted.
   - Never remove or rename existing fields without a formal deprecation period and API versioning (`/v2/`).

---

## 2. Consumer-Driven Contract Testing (Pact)

Consumer-Driven Contracts reverse the traditional provider-first approach:
1. The **Consumer** defines the minimal interaction expectations (request shape + expected response).
2. The contract file (Pact JSON) is published to the Pact Broker.
3. The **Provider** runs automated verification against the contract to confirm it satisfies all consumers.

```typescript
// Consumer interaction test (Pact)
await provider
  .given("User with ID 42 exists")
  .uponReceiving("A GET request to /api/users/42")
  .withRequest({
    method: "GET",
    path: "/api/users/42",
    headers: { Accept: "application/json" },
  })
  .willRespondWith({
    status: 200,
    headers: { "Content-Type": "application/json" },
    body: {
      id: 42,
      email: Matchers.email(),
      name: Matchers.string(),
    },
  });
```
