import requests
import logging
import allure
from features.utils.config import API_BASE_URL
from features.utils.logger import logger

def before_scenario(context, scenario):
    """
    Before each scenario, check if it requires test accounts.
    Additionally, ensure a specific balance exists for withdrawal scenarios.
    """

    # Create test accounts if required
    if any(keyword in scenario.name.lower() for keyword in ["existing account", "debit account", "credit account", "transfer money"]):
        create_test_accounts(context)


def create_test_accounts(context):
    """Creates debit & credit accounts before tests that need them."""
    url = f"{API_BASE_URL}/account"
    payload = {"currency": "USD"}

    # Create debit account
    logger.info("Creating a test debit account before scenario execution...")
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"Failed to create test debit account. Response: {response.text}"
    context.debit_account_id = response.json().get("id")
    logger.info(f"Test debit account created with ID: {context.debit_account_id}")

    # Create credit account
    logger.info("Creating a test credit account before scenario execution...")
    response = requests.post(url, json=payload)
    assert response.status_code == 201, f"Failed to create test credit account. Response: {response.text}"
    context.credit_account_id = response.json().get("id")
    logger.info(f"Test credit account created with ID: {context.credit_account_id}")
