# Behavior-Driven Development (BDD) & Living Documentation

**Behavior-Driven Development (BDD)** bridges the communication gap between business requirements, product owners, and engineers through human-readable, executable specifications written in **Gherkin syntax**.

---

## 1. Gherkin Structure & Grammar

```gherkin
Feature: Order Cancellation & Refund Processing
  As an authenticated e-commerce customer
  I want to cancel an order within 30 minutes of creation
  So that I can recover my funds if I made a mistake

  Background:
    Given the store has a 30-minute cancellation policy
    And customer "Alice" has an active account

  Scenario: Customer cancels an unfulfilled order within the grace period
    Given Alice placed order "ORD-1234" 15 minutes ago
    And the order status is "PENDING_FULFILLMENT"
    When Alice requests cancellation for order "ORD-1234"
    Then the order status must transition to "CANCELLED"
    And a full refund of 150.00 BRL must be scheduled
    And an email confirmation must be queued for Alice

  Scenario Outline: Illegal state transitions are rejected
    Given Alice has an order with status "<initial_status>"
    When Alice requests cancellation for the order
    Then the request must be rejected with error "<error_code>"
    And the order status must remain "<initial_status>"

    Examples:
      | initial_status | error_code             |
      | SHIPPED        | CANNOT_CANCEL_SHIPPED  |
      | DELIVERED      | CANNOT_CANCEL_DELIVERED|
      | CANCELLED      | ALREADY_CANCELLED      |
```

---

## 2. Best Practices for BDD Scenarios

1. **Focus on Business Invariants, not UI Clicks:**
   - ❌ *Avoid:* "When I click the red button on `#submit-btn` at coordinate (100, 200)"
   - ✅ *Prefer:* "When Alice requests cancellation for order 'ORD-1234'"
2. **Deterministic Preconditions:**
   - Always state the initial state machine condition explicitly in the `Given` clause.
3. **One Logical Outcome per Scenario:**
   - Keep assertions focused on the invariant under test.
