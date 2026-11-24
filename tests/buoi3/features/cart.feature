Feature: Shopping cart
  As a shopper
  I want to add the quantity of tools I need
  So that I can check the correct cost before checkout

  Background:
    Given I am on the home page

  Scenario Outline: Cart prices reflect the selected product and quantity
    When I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I open the cart
    Then the cart contains "<product>"
    And the line price equals the unit price times <quantity>
    And the cart total equals the sum of the line prices

    Examples:
      | product            | quantity |
      | Combination Pliers | 1        |
      | Claw Hammer        | 3        |
