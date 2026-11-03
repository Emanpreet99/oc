"""T002: Shopping Cart (F2) - add, change quantity, remove, empty cart."""
from selenium.webdriver.common.by import By

from common.pages import add_first_product_to_cart, url, wait_for
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_add_to_cart_success(driver):
    # Add the first product and check that the store confirms it was added.
    msg = add_first_product_to_cart(driver)
    assert "Success: You have added" in msg

    # Open the shopping cart and confirm it contains the iPhone.
    driver.get(url("checkout/cart"))
    assert "iPhone" in driver.find_element(By.ID, "content").text


def test_update_quantity(driver):
    # Add a product, then open the cart page.
    add_first_product_to_cart(driver)
    driver.get(url("checkout/cart"))

    # Change the product quantity to 3 and submit the update.
    qty = wait_for(driver, (By.CSS_SELECTOR, "input[name^='quantity']"))
    qty.clear()
    qty.send_keys("3")
    driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Update']").click()

    # Wait for the quantity field to show the updated value.
    qty = wait_for(driver, (By.CSS_SELECTOR, "input[name^='quantity']"))
    assert qty.get_attribute("value") == "3"

    # Confirm that the store displays a successful update message.
    assert "Success: You have modified your shopping cart!" in driver.find_element(
        By.CSS_SELECTOR, ".alert-success").text

def test_remove_item_gives_empty_cart(driver):
    # Add a product, open the cart, and remove the item.
    add_first_product_to_cart(driver)
    driver.get(url("checkout/cart"))
    wait_for(driver, (By.CSS_SELECTOR, "button[data-original-title='Remove']")).click()

    # Wait until the cart page reports that it is empty.
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "content"), "Your shopping cart is empty!"
        )
    )

def test_empty_cart_shows_message_for_new_session(driver):
    # Open the cart without adding anything and check the empty-cart message.
    driver.get(url("checkout/cart"))
    assert "Your shopping cart is empty!" in wait_for(
        driver, (By.CSS_SELECTOR, "#content p")).text
