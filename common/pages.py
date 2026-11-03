"""Shared helpers for all OpenCart tests (locators + reusable actions)."""
import os
import time
import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("BASE_URL", "https://opencart.abstracta.us/index.php?route=")
TIMEOUT = 10
SHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")


def url(route: str) -> str:
    """Build a full page URL from an OpenCart route, e.g. 'account/login'."""
    return BASE_URL + route


def wait_for(driver, locator, timeout=TIMEOUT):
    """Wait until an element is visible and return it."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def shot(driver, name: str):
    """Save a screenshot into /screenshots (used as evidence in the report)."""
    os.makedirs(SHOT_DIR, exist_ok=True)
    driver.save_screenshot(os.path.join(SHOT_DIR, f"{name}.png"))


def register_new_user(driver):
    """Register a unique throw-away account (this also logs the user in).
    Returns (email, password)."""
    email = f"test_{uuid.uuid4().hex[:10]}@example.com"
    password = "Passw0rd!23"
    driver.get(url("account/register"))
    driver.find_element(By.ID, "input-firstname").send_keys("Test")
    driver.find_element(By.ID, "input-lastname").send_keys("User")
    driver.find_element(By.ID, "input-email").send_keys(email)
    driver.find_element(By.ID, "input-telephone").send_keys("0400000000")
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.ID, "input-confirm").send_keys(password)
    driver.find_element(By.NAME, "agree").click()
    driver.find_element(By.CSS_SELECTOR, "input[value='Continue']").click()
    wait_for(driver, (By.CSS_SELECTOR, "#content h1"))
    return email, password


def add_first_product_to_cart(driver, search_term="iphone"):
    """Search for a product and click Add to Cart on the first result."""
    driver.get(url(f"product/search&search={search_term}"))
    btn = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".product-layout button[onclick*='cart.add']")))
    btn.click()
    return wait_for(driver, (By.CSS_SELECTOR, ".alert-success")).text


def clear_cart(driver):
    """Remove every item from the cart (keeps tests independent)."""
    driver.get(url("checkout/cart"))
    while driver.find_elements(By.CSS_SELECTOR, "button[data-original-title='Remove']"):
        driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Remove']").click()
        time.sleep(1.5)
        driver.get(url("checkout/cart"))
