-- ============================================================================
-- Example: Data-Driven Design (DataDD) in PostgreSQL
-- Core Principles:
-- 1. Access Patterns Matrix first
-- 2. ESR Indexing Rule (Equality, Sort, Range)
-- 3. Covering Indexes (INCLUDE) to eliminate heap fetches
-- 4. Optimistic Locking with atomic version increments
-- ============================================================================

-- ACCESS PATTERNS MATRIX:
-- Q1: Fetch active customer orders sorted by creation (2,500 ops/sec, SLA < 10ms)
-- Q2: Look up order details by idempotency key (800 ops/sec, SLA < 5ms)
-- Q3: Concurrently debit account balance (400 ops/sec, SLA < 15ms)

CREATE TABLE accounts (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    balance_cents BIGINT NOT NULL DEFAULT 0 CHECK (balance_cents >= 0),
    version INT NOT NULL DEFAULT 1,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_accounts PRIMARY KEY (id)
);

CREATE TABLE orders (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    customer_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL,
    total_cents BIGINT NOT NULL CHECK (total_cents > 0),
    idempotency_key VARCHAR(64) NOT NULL,
    version INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_orders PRIMARY KEY (id),
    CONSTRAINT uq_orders_idempotency UNIQUE (tenant_id, idempotency_key)
);

-- Q1 Optimized Index (Rule ESR: Equality on tenant_id + customer_id, Sort on created_at DESC)
-- Uses INCLUDE to achieve Index Only Scan (eliminates visiting the heap table)
CREATE INDEX idx_orders_customer_created_covering
ON orders (tenant_id, customer_id, created_at DESC)
INCLUDE (status, total_cents);

-- Q3 Optimistic Locking Atomic Mutation (Lost Update Prevention)
-- Application checks that rows_affected == 1:
-- UPDATE accounts
-- SET balance_cents = balance_cents - :amount_cents,
--     version = version + 1,
--     updated_at = NOW()
-- WHERE id = :account_id
--   AND version = :current_version
--   AND balance_cents >= :amount_cents;
