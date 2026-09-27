/**
 * Example: Type-Driven Design (TypeDD) in TypeScript
 * Core Principles:
 * 1. "Make illegal states unrepresentable" (Yaron Minsky)
 * 2. "Parse, don't validate" (Alexis King)
 * 3. Nominal typing with Branded Types
 * 4. Exhaustive pattern matching with assertNever
 */

// 1. Branded Nominal Identifiers
declare const brand: unique symbol;
export type Brand<T, B> = T & { readonly [brand]: B };

export type OrderId = Brand<string, 'OrderId'>;
export type CustomerId = Brand<string, 'CustomerId'>;
export type TransactionId = Brand<string, 'TransactionId'>;
export type PositiveCents = Brand<number, 'PositiveCents'>;

// 2. Smart Constructors ("Parse, don't validate")
export function parsePositiveCents(amount: number): PositiveCents {
  if (!Number.isInteger(amount) || amount <= 0) {
    throw new Error(`Amount must be a positive integer in cents. Received: ${amount}`);
  }
  return amount as PositiveCents;
}

export function parseOrderId(raw: string): OrderId {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(raw)) {
    throw new Error(`Invalid OrderId format. Must be a valid UUID. Received: ${raw}`);
  }
  return raw as OrderId;
}

// 3. Hermetic State Machine (Zero Illegal States)
export type OrderState =
  | {
      readonly status: 'draft';
      readonly orderId: OrderId;
      readonly customerId: CustomerId;
      readonly totalCents: PositiveCents;
    }
  | {
      readonly status: 'paid';
      readonly orderId: OrderId;
      readonly customerId: CustomerId;
      readonly totalCents: PositiveCents;
      readonly transactionId: TransactionId;
      readonly paidAt: Date;
    }
  | {
      readonly status: 'cancelled';
      readonly orderId: OrderId;
      readonly customerId: CustomerId;
      readonly cancelReason: string;
      readonly cancelledAt: Date;
    };

// 4. Exhaustive Check Helper
export function assertNever(x: never): never {
  throw new Error(`Unhandled state variant: ${JSON.stringify(x)}`);
}

// 5. Pure Transition Functions
export function payOrder(
  order: Extract<OrderState, { status: 'draft' }>,
  transactionId: TransactionId,
  paidAt: Date = new Date()
): Extract<OrderState, { status: 'paid' }> {
  return {
    status: 'paid',
    orderId: order.orderId,
    customerId: order.customerId,
    totalCents: order.totalCents,
    transactionId,
    paidAt,
  };
}

export function cancelOrder(
  order: Extract<OrderState, { status: 'draft' }>,
  reason: string,
  cancelledAt: Date = new Date()
): Extract<OrderState, { status: 'cancelled' }> {
  return {
    status: 'cancelled',
    orderId: order.orderId,
    customerId: order.customerId,
    cancelReason: reason,
    cancelledAt,
  };
}

// 6. Exhaustive Formatter
export function formatOrderStatus(order: OrderState): string {
  switch (order.status) {
    case 'draft':
      return `Order ${order.orderId} is awaiting payment for amount: ${order.totalCents} cents`;
    case 'paid':
      return `Order ${order.orderId} paid at ${order.paidAt.toISOString()} (Tx: ${order.transactionId})`;
    case 'cancelled':
      return `Order ${order.orderId} cancelled at ${order.cancelledAt.toISOString()}: ${order.cancelReason}`;
    default:
      return assertNever(order);
  }
}
