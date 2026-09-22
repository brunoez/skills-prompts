/**
 * TDD Red-Green-Refactor Lifecycle Example.
 * Demonstrates AAA pattern, invariant testing, and edge case coverage.
 */

import { describe, expect, it } from "vitest";

// Domain Value Object under TDD
interface DiscountRule {
  minItems: number;
  percentage: number;
}

function calculateTieredDiscount(totalCents: number, itemCount: number, rules: DiscountRule[]): number {
  if (totalCents < 0 || itemCount < 0) {
    throw new RangeError("Negative totals or item counts are forbidden");
  }
  if (itemCount === 0 || totalCents === 0) return 0;

  // Find the highest applicable discount rule
  const applicable = rules
    .filter((r) => itemCount >= r.minItems)
    .sort((a, b) => b.percentage - a.percentage)[0];

  if (!applicable) return 0;

  return Math.round((totalCents * applicable.percentage) / 100);
}

describe("calculateTieredDiscount", () => {
  const standardRules: DiscountRule[] = [
    { minItems: 3, percentage: 10 },
    { minItems: 5, percentage: 20 },
  ];

  it("should return 0 discount when items are below minimum threshold", () => {
    // Arrange
    const total = 5000;
    const items = 2;

    // Act
    const discount = calculateTieredDiscount(total, items, standardRules);

    // Assert
    expect(discount).toBe(0);
  });

  it("should apply 10% discount when item count meets the 3 items tier", () => {
    // Arrange
    const total = 6000;
    const items = 3;

    // Act
    const discount = calculateTieredDiscount(total, items, standardRules);

    // Assert
    expect(discount).toBe(600);
  });

  it("should apply 20% discount when item count meets the 5 items tier", () => {
    // Arrange
    const total = 10000;
    const items = 5;

    // Act
    const discount = calculateTieredDiscount(total, items, standardRules);

    // Assert
    expect(discount).toBe(2000);
  });

  it("should throw RangeError when total is negative (defensive invariant)", () => {
    expect(() => calculateTieredDiscount(-100, 3, standardRules)).toThrow(RangeError);
  });
});
