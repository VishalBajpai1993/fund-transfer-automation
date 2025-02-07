Feature: Account Management API Testing

  Scenario: Create an account and retrieve it
    Given a request to create an account with currency "USD"
    When the request is sent
    Then the account should be created successfully

    Given the same account ID from the previous step
    When a request is made to retrieve the account
    Then the account details should be returned

  Scenario: Retrieve a non-existent account
    Given a non-existent account ID
    When a request is made to retrieve the account
    Then the response should indicate account not found