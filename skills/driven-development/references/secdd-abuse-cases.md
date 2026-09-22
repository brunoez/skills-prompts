# Security-Driven Development (SecDD) & Abuse Case Testing

**Security-Driven Development (SecDD)** treats security requirements not as an afterthought during pen-testing, but as first-class automated test specifications (Abuse Cases) written alongside business tests.

---

## 1. Evil User Stories & Abuse Cases

For every feature, model the corresponding **Evil User Story**:

| Feature (User Story) | Evil User Story (Abuse Case) | Automated Test Assertion |
| :--- | :--- | :--- |
| As a user, I want to redeem a $50 gift coupon. | As an attacker, I want to send 20 parallel requests to redeem the same single-use coupon simultaneously. | **Concurrency Test:** Exactly 1 request succeeds (200), and 19 requests fail (409 Conflict / 400 Bad Request). Total balance credited is strictly $50. |
| As a tenant, I want to fetch my monthly invoice. | As an attacker from Tenant B, I want to iterate UUIDs and fetch Tenant A's invoice. | **BOLA Test:** Request returns HTTP 403 Forbidden or 404 Not Found. |
| As a customer, I want to update my profile biography. | As an attacker, I want to send `{"role": "admin"}` in the update JSON. | **Mass Assignment Test:** Property `role` is rejected or stripped; user's role remains `customer`. |

---

## 2. Automated Concurrency Abuse Test Pattern (TypeScript / Vitest)

```typescript
test("prevent double spending on single-use discount coupon (TOCTOU)", async () => {
  const couponCode = "ONETIME100";
  const user = await createTestUser();

  // Fire 10 parallel requests simultaneously
  const promises = Array.from({ length: 10 }).map(() =>
    request(app)
      .post("/api/coupons/redeem")
      .set("Authorization", `Bearer ${user.token}`)
      .send({ code: couponCode })
  );

  const responses = await Promise.all(promises);
  const successCount = responses.filter((r) => r.status === 200).length;
  const conflictCount = responses.filter((r) => r.status === 409 || r.status === 400).length;

  // INVARIANT: Exactly 1 redemption allowed
  expect(successCount).toBe(1);
  expect(conflictCount).toBe(9);
});
```
