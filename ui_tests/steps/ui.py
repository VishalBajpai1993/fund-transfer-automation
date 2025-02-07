import time
import allure
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.utils.logger import logger
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from behave import given, when, then

@given("I navigate to the GomSpace website")
@allure.step("Navigating to GomSpace website")
def step_impl(context):
    """Launch Microsoft Edge, open GomSpace website, and handle cookie pop-up if present."""
    logger.info("Initializing Edge WebDriver...")

    # Use Microsoft Edge WebDriver
    context.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

    logger.info("Navigating to GomSpace website: https://gomspace.com")
    context.driver.get("https://gomspace.com")

    # Maximize the window for live visibility
    context.driver.maximize_window()
    
    # Wait for the page to load
    WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Handle Cookie Pop-up if Present
    try:
        logger.info("Checking for cookie consent pop-up...")

        # Wait for the Accept Cookies button to be present and clickable
        accept_cookies_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Allow all cookies')]"))
        )

        if accept_cookies_button.is_displayed():
            logger.info("Cookie pop-up detected. Clicking 'Accept' button.")
            # Attach Screenshot of Accepting Cookies
            allure.attach(context.driver.get_screenshot_as_png(), name="Cookies to be Accepted", attachment_type=allure.attachment_type.PNG)
            
            # Click on Accept Button
            accept_cookies_button.click()

            # Wait for the button to disappear or for the next step to load
            WebDriverWait(context.driver, 5).until(
                EC.invisibility_of_element(accept_cookies_button)
            )

            # Attach Screenshot after Accepting Cookies
            allure.attach(context.driver.get_screenshot_as_png(), name="Cookies Accepted", attachment_type=allure.attachment_type.PNG)
            
            logger.info("Cookie pop-up handled successfully.")

    except Exception as e:
        logger.warning("No cookie consent pop-up found. Proceeding with the test.")
        logger.warning(f"Error: {e}")

    # Attach Screenshot of Homepage
    allure.attach(context.driver.get_screenshot_as_png(), name="Homepage Screenshot", attachment_type=allure.attachment_type.PNG)
    logger.info("GomSpace website opened successfully.")

@when("I go to the Products menu and select a subcategory")
@allure.step("Navigating to Products menu and selecting a subcategory")
def step_impl(context):
    logger.info("Attempting to click on the 'Products' menu.")
    
    try:
        # Wait for the 'Products' menu to be clickable
        products_menu = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='main_title'][normalize-space()='Products']"))
        )
        products_menu.click()
        
        # Wait for the subcategory link to be clickable
        logger.info("Products menu clicked. Selecting a subcategory.")
        subcategory = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='title'][normalize-space()='Power Systems']"))
        )
        subcategory.click()

        # Attach screenshot for debugging
        allure.attach(context.driver.get_screenshot_as_png(), name="Subcategory Selected", attachment_type=allure.attachment_type.PNG)

        logger.info("Subcategory 'Power Systems' selected successfully.")
    
    except Exception as e:
        logger.error(f"Error selecting subcategory: {str(e)}")
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        raise

@then("the number of displayed products should be greater than 0")
@allure.step("Verifying product count is greater than 0")
def step_impl(context):
    logger.info("Checking the number of displayed products.")
    
    try:
        # Wait for product items to be visible
        products = WebDriverWait(context.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "shop_productlistdynamiccolumns"))
        )
        product_count = len(products)
        
        allure.attach(f"Product Count: {product_count}", name="Product Count", attachment_type=allure.attachment_type.TEXT)

        assert product_count > 0, f"Expected at least 1 product, but found {product_count}"
        
        logger.info(f"Product verification successful. Found {product_count} products.")

    except Exception as e:
        logger.error(f"Error verifying product count: {str(e)}")
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        raise

@then("each product should have a title and description")
@allure.step("Verifying each product has a title and description")
def step_impl(context):
    logger.info("Checking each product for title and description.")
    
    try:
        # Wait for the products to be visible
        products = WebDriverWait(context.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "shop_productlistdynamiccolumns"))
        )
        
        for product in products:
            try:
                title = product.find_element(By.CLASS_NAME, "name").text
                description = product.find_element(By.CLASS_NAME, "teaser").text
                
                allure.attach(f"Title: {title}, Description: {description}", name="Product Details", attachment_type=allure.attachment_type.TEXT)
                
                assert title, "Product title is missing"
                assert description, "Product description is missing"
                
                logger.info(f"Verified product: {title} - {description}")
            
            except Exception as e:
                logger.error(f"Error verifying product details: {str(e)}")
                allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
                raise

    except Exception as e:
        logger.error(f"Error verifying products: {str(e)}")
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        raise

@when('I click on the "Read more" button for a product')
@allure.step("Clicking 'Read more' button")
def step_impl(context):
    logger.info("Clicking on 'Read more' button for a product.")
    
    try:
        # Locate the 'Read more' button first
        read_more_button = context.driver.find_element(By.XPATH, "//div[@class='shop_productlistcolumn_item itemno1']//span[contains(text(),'Read more')]")
        
        # Scroll incrementally by a percentage (20%) until the element is visible
        max_scrolls = 5  # Define the maximum number of scrolls
        scrolls = 0
        while scrolls < max_scrolls:
            # Scroll down by a small percentage of the page height (e.g., 20%)
            context.driver.execute_script("window.scrollBy(0, window.innerHeight * 0.2);")
            time.sleep(1)  # Give the page some time to load content
            
            # Check if the 'Read more' button is in the viewport
            if read_more_button.is_displayed():
                logger.info("Found 'Read more' button in view.")
                break

            scrolls += 1
        # Attach screenshot before clicking 'Read More'
        allure.attach(context.driver.get_screenshot_as_png(), name="Read More is visible to click", attachment_type=allure.attachment_type.PNG)

        # Wait for the 'Read more' button to be clickable after scrolling
        WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='shop_productlistcolumn_item itemno1']//span[contains(text(),'Read more')]"))
        )

        # Click the 'Read more' button
        read_more_button.click()

        # Attach screenshot after clicking 'Read More'
        allure.attach(context.driver.get_screenshot_as_png(), name="Read More Clicked", attachment_type=allure.attachment_type.PNG)

        logger.info("Clicked on 'Read more' button successfully.")
    
    except Exception as e:
        logger.error(f"Error clicking 'Read more': {str(e)}")
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        raise

@then("I should be navigated to the product details page")
@allure.step("Verifying product details page")
def step_impl(context):
    logger.info("Verifying product details page is displayed.")
    
    try:
        # Wait for the 'Add to quote request' button to be visible
        add_to_quote_button = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Add to quote request']"))
        )
        
        # Scroll to the 'Add to quote request' button to ensure it's visible
        context.driver.execute_script("arguments[0].scrollIntoView(true);", add_to_quote_button)

        # Verify the product detail page by checking the button or any relevant information
        product_detail_header = add_to_quote_button.text
        
        allure.attach(product_detail_header, name="Product Detail Page Header", attachment_type=allure.attachment_type.TEXT)

        assert product_detail_header, "Product details page not loaded properly"

        # Attach screenshot of the product details page
        allure.attach(context.driver.get_screenshot_as_png(), name="Product Details Page", attachment_type=allure.attachment_type.PNG)

        logger.info(f"Successfully navigated to the product details page: {product_detail_header}")
    
    except Exception as e:
        logger.error(f"Error verifying product details page: {str(e)}")
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        raise

@then("I close the browser")
@allure.step("Closing the browser")
def step_impl(context):
    logger.info("Closing the browser.")
    
    try:
        if context.driver:
            context.driver.quit()
            logger.info("Browser closed successfully.")
        else:
            logger.warning("Browser was already closed.")
    
    except Exception as e:
        logger.error(f"Error closing the browser: {str(e)}")
        allure.attach(str(e), name="Error Details", attachment_type=allure.attachment_type.TEXT)
        raise

