from behave import given, when, then
import requests
import logging
import allure
from features.utils.config import API_BASE_URL
from features.utils.logger import logger

# ================================
# Deposit Money Steps (With Full API Logs)
# ================================

@given("an existing account")
@allure.step("Given an existing account")
def step_impl(context):
    """Automatically create an account before the deposit request."""
    payload = {"currency": "USD"}
    
    response = requests.post(f"{API_BASE_URL}/account", json=payload)
    assert response.status_code == 201, f"Failed to create account. Response: {response.text}"
    
    context.account_id = response.json().get("id")
    logger.info(f"Created test account with ID: {context.account_id}")

    # Attach API response to Allure
    allure.attach(str(response.json()), name="Created Account", attachment_type=allure.attachment_type.JSON)

@given("an invalid account ID")
@allure.step("Given an invalid account ID")
def step_impl(context):
    context.account_id = "999999999"
    logger.info(f"Using non-existent account ID: {context.account_id}")

@when("a deposit request is made with amount {amount} and currency \"{currency}\"")
@allure.step("When a deposit request is made with amount {amount} and currency {currency}")
def step_impl(context, amount, currency):
    """Sends a deposit request and stores the response for validation in the next step."""
    payload = {"accountId": context.account_id, "amount": float(amount), "currency": currency}

    # Attach request payload to Allure
    allure.attach(str(payload), name="Deposit Request Payload", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Sending deposit request: {payload}")
    context.response = requests.post(f"{API_BASE_URL}/transaction/deposit", json=payload)

    # Attach response details to Allure
    allure.attach(f"Status Code: {context.response.status_code}", name="Deposit API Response Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(str(context.response.text), name="Deposit API Response Body", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Deposit Response: {context.response.status_code} - {context.response.text}")

@then("the deposit should be successful")
@allure.step("Then the deposit should be successful")
def step_impl(context):
    """Validates that the deposit request was successful (status code 200)."""
    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}"

@then("the deposit should fail with status {status_code}")
@allure.step("Then the deposit should fail with status {status_code}")
def step_impl(context, status_code):
    """Validates that the deposit request failed with the expected status code (400 or 404)."""
    assert context.response.status_code == int(status_code), f"Expected {status_code} but got {context.response.status_code}"

# ================================
# Withdraw Money Steps (With Full API Logs)
# ================================

@given("account with ID {account_id} and a balance of {balance}")
@allure.step("Given an account with ID {account_id} and balance {balance}")
def step_impl(context, account_id, balance):
    context.account_id = account_id
    context.balance = float(balance)
    logger.info(f"Using account ID {account_id} with balance {balance}")

@when("a withdraw request is made with amount {amount} and currency \"{currency}\"")
@allure.step("When a withdraw request is made with amount {amount} and currency {currency}")
def step_impl(context, amount, currency):
    """Sends a withdrawal request and stores the response."""
    payload = {"accountId": context.account_id, "amount": float(amount), "currency": currency}

    # Attach request details to Allure
    allure.attach(str(payload), name="Withdraw Request Payload", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Sending withdrawal request: {payload}")
    context.response = requests.post(f"{API_BASE_URL}/transaction/withdraw", json=payload)

    # Attach response to Allure for debugging
    allure.attach(str(context.response.status_code), name="Withdraw API Response Code", attachment_type=allure.attachment_type.TEXT)
    allure.attach(context.response.text, name="Withdraw API Response Body", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Response: {context.response.status_code} - {context.response.text}")

@then("the withdrawal should be successful")
@allure.step("Then the withdrawal should be successful")
def step_impl(context):
    """Asserts that the withdrawal request was successful (200 OK)."""
    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}"

@then("the withdrawal should fail with status {status_code}")
@allure.step("Then the withdrawal should fail with status {status_code}")
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code), f"Expected {status_code} but got {context.response.status_code}"

# ================================
# Transfer Money Steps (With Full API Logs)
# ================================

@allure.step("Given an existing debit account")
@given("an existing debit account")
def step_impl(context):
    """Uses pre-created debit account."""
    context.debit_account = {"id": context.debit_account_id}
    logger.info(f"Using debit account ID {context.debit_account_id}")
    allure.attach(
        str(context.debit_account),
        name="Debit Account Details",
        attachment_type=allure.attachment_type.JSON
    )

@allure.step("Given an existing credit account")
@given("an existing credit account")
def step_impl(context):
    """Uses pre-created credit account."""
    context.credit_account = {"id": context.credit_account_id}
    logger.info(f"Using credit account ID {context.credit_account_id}")
    allure.attach(
        str(context.credit_account),
        name="Credit Account Details",
        attachment_type=allure.attachment_type.JSON
    )
@allure.step("Given a non-existent debit account")
@given("a non-existent debit account")
def step_impl(context):
    """Uses an invalid debit account ID."""
    context.debit_account = {"id": "999999999"}  # Invalid account ID
    logger.info("Using non-existent debit account ID 999999999")

@allure.step("Given a non-existent credit account")
@given("a non-existent credit account")
def step_impl(context):
    """Uses an invalid credit account ID."""
    context.credit_account = {"id": "999999999"}  # Invalid account ID
    logger.info("Using non-existent credit account ID 999999999")

@allure.step("Given an existing debit account with balance {balance} in {currency}")
@given("an existing debit account with balance {balance} in \"{currency}\"")
def step_impl(context, balance, currency):
    """Creates a debit account with a specific balance and currency."""
    
    # Step 1: Create a new debit account
    create_response = requests.post(f"{API_BASE_URL}/account", json={"currency": currency})
    assert create_response.status_code == 201, f"Failed to create debit account. Response: {create_response.text}"
    
    # Extract account ID
    account_id = create_response.json().get("id")
    context.debit_account_id = account_id  # Store in context

    logger.info(f"Created new debit account with ID: {account_id} in {currency}")

    # Step 2: Fund the account with the specified balance
    deposit_payload = {"accountId": account_id, "amount": float(balance), "currency": currency}
    deposit_response = requests.post(f"{API_BASE_URL}/transaction/deposit", json=deposit_payload)

    assert deposit_response.status_code == 200, f"Failed to deposit money. Response: {deposit_response.text}"
    logger.info(f"Deposited {balance} {currency} into account {account_id}")

    # Store account details in context
    context.debit_account = {
        "id": account_id,
        "balance": float(balance),
        "currency": currency
    }

    # Attach API request & response data to Allure for debugging
    allure.attach(str(create_response.json()), name="Debit Account Creation Response", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(deposit_payload), name="Deposit Request Payload", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(deposit_response.json()), name="Deposit API Response", attachment_type=allure.attachment_type.JSON)

@allure.step("When a transfer request is made with amount {amount} and currency {currency}")
@when("a transfer request is made with amount {amount} and currency \"{currency}\"")
def step_impl(context, amount, currency):
    """Sends a transfer request and stores the response."""
    payload = {
        "debitAccountId": context.debit_account["id"],
        "creditAccountId": context.credit_account["id"],
        "amount": float(amount),
        "currency": currency
    }

    # Attach request details to Allure
    allure.attach(str(payload), name="Transfer Request Payload", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Sending transfer request: {payload}")
    context.response = requests.post(f"{API_BASE_URL}/transaction/transfer", json=payload)

    # Attach response details to Allure
    allure.attach(str(context.response.text), name="Transfer API Response", attachment_type=allure.attachment_type.JSON)
    logger.info(f"Response: {context.response.status_code} - {context.response.text}")

@allure.step("Then the transfer should be successful")
@then("the transfer should be successful")
def step_impl(context):
    """Asserts that the transfer request was successful (200 OK)."""

    #Attach full API response for debugging
    allure.attach(
        f"Status Code: {context.response.status_code}",
        name="Transfer API Status Code",
        attachment_type=allure.attachment_type.TEXT
    )

    try:
        response_json = context.response.json()
        allure.attach(
            str(response_json),
            name="Transfer API Response (Successful)",
            attachment_type=allure.attachment_type.JSON
        )
        logger.info(f"Transfer success response: {response_json}")
    except requests.exceptions.JSONDecodeError:
        allure.attach(
            context.response.text,
            name="Transfer API Response (Invalid JSON)",
            attachment_type=allure.attachment_type.TEXT
        )
        logger.error(f"Transfer API returned invalid JSON: {context.response.text}")

    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}"


@allure.step("Then the transfer should fail with status {status_code}")
@then("the transfer should fail with status {status_code}")
def step_impl(context, status_code):
    """Asserts that the transfer request failed with the expected status code."""

    #Attach full API response for debugging
    allure.attach(
        f"Status Code: {context.response.status_code}",
        name="Transfer API Status Code",
        attachment_type=allure.attachment_type.TEXT
    )

    try:
        response_json = context.response.json()
        allure.attach(
            str(response_json),
            name=f"Transfer API Response (Failure {status_code})",
            attachment_type=allure.attachment_type.JSON
        )
        logger.info(f"Transfer failure response: {response_json}")
    except requests.exceptions.JSONDecodeError:
        allure.attach(
            context.response.text,
            name=f"Transfer API Response (Invalid JSON for {status_code})",
            attachment_type=allure.attachment_type.TEXT
        )
        logger.error(f"Transfer API returned invalid JSON: {context.response.text}")

    assert context.response.status_code == int(status_code), f"Expected {status_code} but got {context.response.status_code}"
