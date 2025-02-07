Feature: GomSpace Web UI Testing

  Scenario: Verify product listing
    Given I navigate to the GomSpace website
    When I go to the Products menu and select a subcategory
    Then the number of displayed products should be greater than 0
    And each product should have a title and description

  Scenario: Verify product details page
    Given I navigate to the GomSpace website
    When I go to the Products menu and select a subcategory
    And I click on the "Read more" button for a product
    Then I should be navigated to the product details page
