from selenium import webdriver

def before_all(context):
    context.driver = None

def after_scenario(context, scenario):
    if context.driver:
        context.driver.quit()