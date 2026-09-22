/**
 * Spec-Driven Development Example: Single Source of Truth with Zod.
 * Defines runtime validation, boundary limits, and compile-time type inference.
 */

import { z } from "zod";

export const TransferFundsInputSchema = z
  .object({
    sourceAccountId: z.string().uuid("Source account must be a valid UUID"),
    destinationAccountId: z.string().uuid("Destination account must be a valid UUID"),
    amountCents: z
      .number()
      .int("Amount must be in integer cents")
      .positive("Amount must be greater than zero")
      .max(10_000_000, "Single transfer limit is 100,000.00"),
    currency: z.enum(["BRL", "USD", "EUR"]).default("BRL"),
    idempotencyKey: z
      .string()
      .min(16, "Idempotency key must have at least 16 characters")
      .max(128),
    memo: z.string().max(140, "Memo length exceeded").optional(),
  })
  .strict() // Prevents unexpected properties (anti-Mass Assignment)
  .refine(
    (data) => data.sourceAccountId !== data.destinationAccountId,
    {
      message: "Source and destination accounts must be distinct",
      path: ["destinationAccountId"],
    }
  );

export type TransferFundsInput = z.infer<typeof TransferFundsInputSchema>;
