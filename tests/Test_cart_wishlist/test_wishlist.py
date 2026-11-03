"""T003: Wish List (F3) - needs a registered, logged-in user (created by the logged_in_driver fixture)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.pages import url, wait_for

def test_logged_in_user_removes_item(logged_in_driver):
    """Removing an item leaves the wish list empty."""
    d = logged_in_driver
    _click_wishlist_on_first_result(d)
    d.get(url("account/wishlist"))

    remove_link = wait_for(
        d, (By.CSS_SELECTOR, "a[data-original-title='Remove']")
    )
    remove_link.click()

    WebDriverWait(d, 10).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "a[data-original-title='Remove']")
        )
    )
    assert not d.find_elements(
        By.CSS_SELECTOR, "a[data-original-title='Remove']"
    )


def test_new_account_has_empty_wishlist(logged_in_driver):
    """A new account starts with no saved wishlist items."""
    d = logged_in_driver
    d.get(url("account/wishlist"))

    assert d.title == "My Wish List"
    assert not d.find_elements(
        By.CSS_SELECTOR, "a[data-original-title='Remove']"
    )


def _click_wishlist_on_first_result(driver, term="iphone"):
    driver.get(url(f"product/search&search={term}"))
    btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".product-layout button[onclick*='wishlist.add']")))
    btn.click()
    return wait_for(driver, (By.CSS_SELECTOR, ".alert")).text


def test_guest_cannot_save_to_wishlist(driver):
    """Failure case: a guest is told to log in."""
    msg = _click_wishlist_on_first_result(driver)
    assert "You must login or create an account" in msg


def test_logged_in_user_adds_item(logged_in_driver):
    """Success case: item appears in wish list page."""
    d = logged_in_driver
    msg = _click_wishlist_on_first_result(d)
    assert "Success: You have added" in msg
    d.get(url("account/wishlist"))
    assert "iPhone" in wait_for(d, (By.ID, "content")).text


""" def test_logged_in_user_removes_item(logged_in_driver):
    #Success case: removing the item empties the wish list.
    d = logged_in_driver
    _click_wishlist_on_first_result(d)
    d.get(url("account/wishlist"))
    print("Wishlist URL:", d.current_url)
    print("Page title:", d.title)
    print("Page text:", d.find_element(By.ID, "content").text)
    wait_for(d, (By.CSS_SELECTOR, "a[data-original-title='Remove']")).click()
    assert "Your wish list is empty" in wait_for(d, (By.CSS_SELECTOR, "#content p")).text """

def test_logged_in_user_removes_item(logged_in_driver):
    """Removing an item leaves the wish list empty."""
    d = logged_in_driver
    _click_wishlist_on_first_result(d)
    d.get(url("account/wishlist"))

    remove_link = wait_for(
        d, (By.CSS_SELECTOR, "a[data-original-title='Remove']")
    )
    remove_link.click()

    WebDriverWait(d, 10).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "a[data-original-title='Remove']")
        )
    )
    assert not d.find_elements(
        By.CSS_SELECTOR, "a[data-original-title='Remove']"
    )

