"""T001: Product Search (F1) - 3+ inputs, success and failure cases."""
import pytest
from selenium.webdriver.common.by import By

from common.pages import url, wait_for

NO_RESULT_MSG = "There is no product that matches the search criteria."


@pytest.mark.parametrize("term, should_find, expected_title", [
    ("iphone",   True,  "iPhone"),          # success: exact product name
    ("IPHONE",   True,  "iPhone"),          # success: search is case-insensitive
    ("macbook",  True,  "MacBook"),         # success: another valid product
    ("zzz_nope", False, None),              # failure: nothing matches
    ("   ",      False, None),              # failure: whitespace only
])
def test_search_from_search_box(driver, term, should_find, expected_title):
    driver.get(url("common/home"))
    box = wait_for(driver, (By.NAME, "search"))        # header search input
    box.clear()
    box.send_keys(term)
    driver.find_element(By.CSS_SELECTOR, "#search button").click()  # magnifier

    wait_for(driver, (By.CSS_SELECTOR, "#content"))
    titles = [e.text for e in driver.find_elements(By.CSS_SELECTOR, ".product-layout h4 a")]

    if should_find:
        assert any(expected_title.lower() in t.lower() for t in titles), \
            f"'{expected_title}' not in results {titles}"
    else:
        if term.strip():
            # A nonblank search with no matches should have no product cards.
            assert titles == [], f"Expected no products but got {titles}"
        else:
            # This site treats whitespace as an empty search and shows products.
            assert titles, "Expected products for an empty search"


def test_search_results_can_open_product_page(driver):
    """Success: clicking a search result opens that product's detail page."""
    driver.get(url("product/search&search=macbook"))
    link = wait_for(driver, (By.CSS_SELECTOR, ".product-layout h4 a"))
    name = link.text
    link.click()
    assert name in wait_for(driver, (By.CSS_SELECTOR, "#content h1")).text
