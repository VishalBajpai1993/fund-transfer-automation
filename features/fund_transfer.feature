Feature: Fund Transfer API Testing

  # ================================
  # Deposit Money Scenarios
  # ================================

  Scenario: Successfully deposit money into an account
    Given an existing account
    When a deposit request is made with amount 100 and currency "USD"
    Then the deposit should be successful

  Scenario: Attempt to deposit with an invalid account ID
    Given an invalid account ID
    When a deposit request is made with amount 100 and currency "USD"
    Then the deposit should fail with status 404

  Scenario: Attempt to deposit a negative amount
    Given an existing account
    When a deposit request is made with amount -50 and currency "USD"
    Then the deposit should fail with status 400

  Scenario: Attempt to deposit with an invalid currency
    Given an existing account
    When a deposit request is made with amount 100 and currency "XYZ"
    Then the deposit should fail with status 400

  # ================================
  # Withdraw Money Scenarios
  # ================================

  Scenario: Successfully withdraw money from an account
    Given an existing account
    When a deposit request is made with amount 500 and currency "USD"
    When a withdraw request is made with amount 100 and currency "USD"
    Then the withdrawal should be successful

  Scenario: Attempt to withdraw with an invalid account ID
    Given an invalid account ID
    When a withdraw request is made with amount 100 and currency "USD"
    Then the withdrawal should fail with status 404

  Scenario: Attempt to withdraw more than the available balance
    Given an existing account
    When a deposit request is made with amount 50 and currency "USD"
    When a withdraw request is made with amount 100 and currency "USD"
    Then the withdrawal should fail with status 400

  Scenario: Attempt to withdraw a negative amount
    Given an existing account
    When a withdraw request is made with amount -50 and currency "USD"
    Then the withdrawal should fail with status 400

  Scenario: Attempt to withdraw with an invalid currency
    Given an existing account
    When a withdraw request is made with amount 100 and currency "XYZ"
    Then the withdrawal should fail with status 400

  # ================================
  # Transfer Money Scenarios
  # ================================

  Scenario: Successfully transfer money from one account to another
    Given an existing debit account with balance 500 in "USD"
    And an existing credit account
    When a transfer request is made with amount 100 and currency "USD"
    Then the transfer should be successful

  Scenario: Attempt to transfer with an invalid debit account
      Given a non-existent debit account
      And an existing credit account
      When a transfer request is made with amount 100 and currency "USD"
      Then the transfer should fail with status 404

  Scenario: Attempt to transfer with an invalid credit account
      Given an existing debit account
      And a non-existent credit account
      When a transfer request is made with amount 100 and currency "USD"
      Then the transfer should fail with status 404