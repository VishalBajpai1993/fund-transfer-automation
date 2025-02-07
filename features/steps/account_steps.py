import requests
import logging
import allure
from behave import given, when, then
from features.utils.config import API_BASE_URL
from features.utils.logger import logger

# # =============================
# Step: Create an Account
# =============================

@allure.step("Given a request to create an account with currency {currency}")
@given("a request to create an account with currency \"{currency}\"")
def step_impl(context, currency):
    context.payload = {"currency": currency}
    logger.info(f"Preparing to create account with currency: {currency}")

@allure.step("When the request is sent to create an account")
@when("the request is sent")
def step_impl(context):
    url = f"{API_BASE_URL}/account"

    logger.info(f"Sending POST request to {url} with payload: {context.payload}")
    context.response = requests.post(url, json=context.payload)

    #Attach request & response data to Allure
    allure.attach(str(context.payload), name="Create Account Request Payload", attachment_type=allure.attachment_type.JSON)
    allure.attach(str(context.response.text), name="Create Account API Response", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Response: {context.response.status_code} - {context.response.text}")

    if context.response.status_code == 201:
        context.account_id = context.response.json().get("id")  # Store account ID for later use

@allure.step("Then the account should be created successfully")
@then("the account should be created successfully")
def step_impl(context):
    assert context.response is not None, "No response received from API"
    assert context.response.status_code == 201, f"Expected 201 but got {context.response.status_code}. Response: {context.response.text}"

    # Store created account ID
    context.account_id = context.response.json().get("id")
    logger.info(f"Account creation successful. ID: {context.account_id}")

    #Attach success response to Allure
    allure.attach(str(context.response.json()), name="Created Account Details", attachment_type=allure.attachment_type.JSON)


# =============================
# Step: Retrieve Created Account
# =============================

@allure.step("Given the same account ID from the previous step")
@given("the same account ID from the previous step")
def step_impl(context):
    assert context.account_id is not None, "No account ID found from previous step"
    logger.info(f"Using created account ID: {context.account_id}")

@allure.step("When a request is made to retrieve the account")
@when("a request is made to retrieve the account")
def step_impl(context):
    url = f"{API_BASE_URL}/account/{context.account_id}"

    logger.info(f"Retrieving account from {url}")
    context.response = requests.get(url)

    #Attach API response to Allure
    allure.attach(str(context.response.text), name="Retrieve Account API Response", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Response: {context.response.status_code} - {context.response.text}")

@allure.step("Then the account details should be returned")
@then("the account details should be returned")
def step_impl(context):
    assert context.response is not None, "No response received from API"
    assert context.response.status_code == 200, f"Expected 200 but got {context.response.status_code}. Response: {context.response.text}"

    account_data = context.response.json()
    assert "id" in account_data, "Account ID missing in response"
    assert "currency" in account_data, "Currency missing in response"
    assert "balance" in account_data, "Balance missing in response"

    logger.info(f"Account details retrieved: {account_data}")

    # Attach retrieved account details to Allure
    allure.attach(str(account_data), name="Retrieved Account Details", attachment_type=allure.attachment_type.JSON)


# ======================================================
# Steps: Retrieve a Non-Existent Account
# ======================================================

@allure.step("Given a non-existent account ID")
@given("a non-existent account ID")
def step_impl(context):
    context.account_id = "999999999"  # A random ID that does not exist
    logger.info(f"Using a non-existent account ID: {context.account_id}")

@allure.step("Then the response should indicate account not found")
@then("the response should indicate account not found")
def step_impl(context):
    assert context.response is not None, "No response received from API"
    assert context.response.status_code == 404, f"Expected 404 but got {context.response.status_code}. Response: {context.response.text}"

    logger.warning("Account not found, as expected.")

    # Attach failed response to Allure for debugging
    allure.attach(str(context.response.text), name="Non-Existent Account Response", attachment_type=allure.attachment_type.JSON)
