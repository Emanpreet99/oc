"""Checkout tests: cart access and billing address."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from common.pages import add_first_product_to_cart, url, wait_for


def test_checkout_with_empty_cart_returns_to_cart(driver):
    """A customer cannot proceed to checkout with an empty cart."""
    driver.get(url("checkout/checkout"))

    WebDriverWait(driver, 10).until(
        lambda d: "checkout/cart" in d.current_url
    )
    assert "Your shopping cart is empty!" in driver.find_element(
        By.ID, "content"
    ).text


def test_logged_in_customer_can_enter_billing_address(logged_in_driver):
    """A logged-in customer can enter a new billing address."""
    d = logged_in_driver
    add_first_product_to_cart(d)
    d.get(url("checkout/checkout"))

    # Wait for the new-address form.
    firstname = wait_for(d, (By.ID, "input-payment-firstname"))
    firstname.clear()
    firstname.send_keys("Test")

    lastname = d.find_element(By.ID, "input-payment-lastname")
    lastname.clear()
    lastname.send_keys("Customer")

    address = d.find_element(By.ID, "input-payment-address-1")
    address.clear()
    address.send_keys("123 Test Street")

    city = d.find_element(By.ID, "input-payment-city")
    city.clear()
    city.send_keys("Los Angeles")

    postcode = d.find_element(By.ID, "input-payment-postcode")
    postcode.clear()
    postcode.send_keys("90001")

# Wait until the United States option is enabled, then select it.
    def united_states_is_enabled(browser):
        country_element = browser.find_element(By.ID, "input-payment-country")
        return any(
            option.text.strip() == "United States" and option.is_enabled()
            for option in Select(country_element).options
        )

    WebDriverWait(d, 10).until(united_states_is_enabled)
    country = Select(d.find_element(By.ID, "input-payment-country"))
    country.select_by_visible_text("United States")

    # Country selection loads the available regions.
    WebDriverWait(d, 10).until(
        lambda browser: len(
            Select(browser.find_element(By.ID, "input-payment-zone")).options
        ) > 1
    )
    zone = Select(d.find_element(By.ID, "input-payment-zone"))
    zone.select_by_visible_text("California")

    d.find_element(By.ID, "button-payment-address").click()

    # The billing address should be accepted and checkout should continue.
    WebDriverWait(d, 10).until(
        EC.presence_of_element_located(
            (By.ID, "collapse-shipping-address")
        )
    )
    assert "checkout/checkout" in d.current_url

def test_checkout_rejects_blank_billing_address(logged_in_driver):
    """Checkout shows validation errors when required billing fields are blank."""
    d = logged_in_driver
    add_first_product_to_cart(d)
    d.get(url("checkout/checkout"))

    # Wait for the billing address form to appear.
    firstname = wait_for(d, (By.ID, "input-payment-firstname"))

    # Clear the required text fields.
    field_ids = [
        "input-payment-firstname",
        "input-payment-lastname",
        "input-payment-address-1",
        "input-payment-city",
        "input-payment-postcode",
    ]
    for field_id in field_ids:
        field = d.find_element(By.ID, field_id)
        field.clear()

    # Submit the blank billing address.
    d.find_element(By.ID, "button-payment-address").click()

    # OpenCart should show validation messages and keep checkout on the page.
    WebDriverWait(d, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".text-danger"))
    )

    errors = d.find_elements(By.CSS_SELECTOR, ".text-danger")
    assert any(error.text.strip() for error in errors)
    assert "checkout/checkout" in d.current_url