# Data-Driven Design (DataDD) Reference Guide

**Data-Driven Design (DataDD)** prioritizes data access patterns, schema normalization trade-offs, and storage engine physics before writing domain or application code. Designing without access patterns leads to premature index bloat, N+1 query storms, and high locking contention under production loads.

---

## 1. The Access Patterns Matrix

Never write a DDL, migration, or collection schema before documenting the target access patterns:

| ID | Description | Target SLA | Frequency | Query Shape | Read/Write |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q1** | Fetch user profile with latest 5 orders | < 15ms | 2,000/s | `WHERE user_id = ? ORDER BY created_at DESC LIMIT 5` | Read Heavy |
| **Q2** | Deduct inventory balance on checkout | < 25ms | 300/s | `UPDATE inventory SET qty = qty - ? WHERE id = ? AND qty >= ?` | High Contention Write |
| **Q3** | Monthly tenant settlement report | < 1,000ms | 1/day | `WHERE tenant_id = ? AND date BETWEEN ? AND ? GROUP BY category` | Analytical Read |

---

## 2. The ESR Indexing Rule (Equality, Sort, Range)

When designing composite B-Tree indexes for relational databases (PostgreSQL, MySQL), always order index columns according to the **ESR principle**:

1. **E - Equality:** Put columns queried with `=` or `IS NULL` first.
2. **S - Sort:** Put columns used in `ORDER BY` second (eliminating expensive in-memory sort / filesort).
3. **R - Range:** Put columns filtered with `>`, `<`, `BETWEEN`, or `LIKE` last (as range scans stop the index traversal for subsequent columns).

```sql
-- Optimal index for: WHERE tenant_id = 'abc' AND status = 'ACTIVE' ORDER BY created_at DESC
CREATE INDEX idx_tenant_status_created 
ON subscriptions (tenant_id, status, created_at DESC);
```

### Covering Indexes (`INCLUDE` in PostgreSQL):
Store frequently retrieved payload columns directly in the index leaf pages to achieve **Index Only Scans** without visiting the heap table:
```sql
CREATE INDEX idx_orders_user_covering 
ON orders (user_id, created_at DESC) 
INCLUDE (status, total_cents);
```

---

## 3. Concurrency & Contention Mitigations

### 1. Optimistic Locking
Use an atomic version increment to prevent Lost Updates without acquiring database table/row locks:
```sql
UPDATE accounts 
SET balance_cents = balance_cents + :delta, version = version + 1
WHERE id = :accountId AND version = :expectedVersion;
```

### 2. Deterministic Lock Ordering (Anti-Deadlock)
When a transaction must update multiple rows, always sort row IDs in ascending alphanumeric order before acquiring row-level locks:
```python
# Prevent deadlocks: Always lock in deterministic order
sorted_ids = sorted([from_account_id, to_account_id])
for acc_id in sorted_ids:
    db.execute("SELECT * FROM accounts WHERE id = ? FOR UPDATE", acc_id)
```
