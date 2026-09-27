# Domain-Driven Design (DDD) Reference Guide

**Domain-Driven Design (DDD)** connects software implementation to an evolving model of core business concepts. It combines **Strategic Design** (large-scale architectural boundaries) with **Tactical Design** (rich, expressive object-oriented or functional domain models).

---

## 1. Strategic Design: Bounded Contexts & Context Mapping

Strategic design prevents monolithic semantic confusion where the same word means different things in different departments.

```mermaid
flowchart LR
    subgraph SalesContext["Sales Context (Upstream)"]
        OrderLead["Lead & Quote"]
    end
    subgraph FulfillmentContext["Fulfillment Context (Downstream)"]
        ShippingOrder["Shipment & Manifest"]
    end
    SalesContext -->|Anti-Corruption Layer (ACL)| FulfillmentContext
```

### Context Mapping Patterns:
* **Shared Kernel:** Shared subset of domain code maintained by two teams (use sparingly).
* **Customer-Supplier / Upstream-Downstream:** Upstream team's changes dictate downstream dependencies.
* **Anti-Corruption Layer (ACL):** An isolating translation layer that translates external models into pure internal domain language, protecting the core from legacy decay.
* **Open Host Service (OHS) / Published Language (PL):** Public protocol (e.g. well-defined OpenAPI/gRPC spec) offered for downstream integrations.

---

## 2. Tactical Design: The Pure Core Building Blocks

### 1. Entities
Objects defined by a persistent identity that runs throughout their lifecycle, rather than their attributes:
```typescript
export class Customer {
  constructor(
    public readonly id: CustomerId,
    private name: string,
    private email: EmailAddress
  ) {}
}
```

### 2. Value Objects
Immutable objects defined exclusively by their attributes, with no conceptual identity. Two Value Objects with identical attributes are equal:
```typescript
export class Money {
  constructor(
    public readonly amountCents: number,
    public readonly currency: 'BRL' | 'USD' | 'EUR'
  ) {
    if (amountCents < 0) throw new Error("Money cannot be negative");
    Object.freeze(this);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) throw new Error("Currency mismatch");
    return new Money(this.amountCents + other.amountCents, this.currency);
  }
}
```

### 3. Aggregates & Aggregate Roots
A cluster of associated objects treated as a single transactional unit for data changes:
* **Root Entity Only:** Outside objects may only hold references to the Aggregate Root.
* **Invariant Protection:** The root guarantees that all business invariants inside the boundary are satisfied on every mutation.
* **One Transaction Rule:** Exactly **one** aggregate is modified per database transaction. Multi-aggregate coordination is handled via Domain Events and eventual consistency.

### 4. Domain Events
Represent immutable facts that occurred in the business past:
```typescript
export interface OrderPlacedEvent {
  readonly eventId: string;
  readonly orderId: OrderId;
  readonly customerId: CustomerId;
  readonly total: Money;
  readonly occurredAt: Date;
}
```
