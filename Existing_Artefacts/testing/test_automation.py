# test_contact_page.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Test Setup ---

@pytest.fixture
def browser():
    """Initializes and quits the browser for each test function."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# --- Test Cases ---

def test_page_titles(browser):
    """
    Test Case TC-NAV-001: Verify that the main navigation links work correctly
    and lead to pages with the correct titles.
    """
    base_url = "http://127.0.0.1:5000"
    pages = {
        "/": "Pharma Inc. - Home",
        "/about": "About - Pharma Inc.",
        "/products": "Products - Pharma Inc.",
        "/contact": "Contact - Pharma Inc."
    }

    for path, title in pages.items():
        browser.get(base_url + path)
        assert title in browser.title

def test_contact_email_display(browser):
    """
    Test Case TC-CONTACT-001: Verify that the contact email address is displayed correctly.
    """
    browser.get("http://127.0.0.1:5000/contact")
    
    email_link = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "footer a"))
    )
    
    assert email_link.text == "contact@pharma-inc.com"
    assert email_link.get_attribute("href") == "mailto:contact@pharma-inc.com"

def test_contact_form_submission_success(browser):
    """
    Test Case TC-CONTACT-002 (Positive): Verify successful form submission with valid data.
    """
    browser.get("http://127.0.0.1:5000/contact")
    
    # Fill out the form
    browser.find_element(By.ID, "name").send_keys("John Doe")
    browser.find_element(By.ID, "email").send_keys("john.doe@example.com")
    browser.find_element(By.ID, "message").send_keys("This is a test inquiry.")
    
    # Submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for the success message
    success_message = WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.ID, "form-status"), "Your inquiry has been sent!")
    )
    assert success_message

def test_contact_form_submission_failure(browser):
    """
    Test Case TC-CONTACT-003 (Negative): Verify form does not submit with an empty required field.
    """
    browser.get("http://127.0.0.1:5000/contact")
    
    # Leave name field blank
    browser.find_element(By.ID, "email").send_keys("jane.doe@example.com")
    browser.find_element(By.ID, "message").send_keys("This is another test.")
    
    # Submit the form
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Check that the success message does not appear
    status_element = browser.find_element(By.ID, "form-status")
    time.sleep(1) # Give a moment to see if text appears
    assert status_element.text == ""

