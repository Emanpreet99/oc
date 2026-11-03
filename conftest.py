"""Pytest fixtures shared by every test folder."""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from common.pages import register_new_user, shot


@pytest.fixture
def driver(request):
    opts = Options()
    opts.add_argument("--window-size=1366,900")
    # opts.add_argument("--headless=new")   # uncomment to run without a window
    drv = webdriver.Chrome(options=opts)     # Selenium Manager fetches the driver
    drv.implicitly_wait(2)
    yield drv
    # Screenshot every test (pass or fail) as report evidence.
    shot(drv, request.node.name.replace("[", "_").replace("]", "").replace(" ", "_"))
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    """A driver that already has a freshly registered, logged-in user."""
    register_new_user(driver)
    return driver
