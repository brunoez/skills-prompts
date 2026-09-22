Feature: Multi-Currency Checkout & Order Authorization
  As an international e-commerce buyer
  I want to authorize payment in my preferred local currency
  So that I have certainty of the final charge amount

  Background:
    Given the product catalog contains item "PROD-TECH-01" priced at 100.00 USD
    And the current exchange rate for BRL is 5.20

  Scenario: Customer completes checkout in BRL with valid funds
    Given customer "Carlos" selects currency "BRL"
    And Carlos adds 2 units of "PROD-TECH-01" to the shopping cart
    When Carlos submits the order for payment authorization
    Then the calculated order total must be 1040.00 BRL
    And payment gateway receives authorization request with amount 104000 cents
    And the order status transitions to "AUTHORIZED"

  Scenario Outline: Checkout is blocked on invalid order inputs
    Given customer selects currency "<currency>"
    And cart contains "<item_quantity>" units of "PROD-TECH-01"
    When customer attempts to submit the order
    Then the checkout is rejected with reason "<error_reason>"
    And no payment authorization is attempted

    Examples:
      | currency | item_quantity | error_reason                  |
      | JPY      | 1             | UNSUPPORTED_CURRENCY          |
      | USD      | 0             | EMPTY_CART                    |
      | USD      | -5            | INVALID_QUANTITY              |
      | BRL      | 150           | EXCEEDS_MAX_ITEMS_PER_ORDER   |
