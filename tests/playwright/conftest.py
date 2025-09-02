import pytest
from playwright.sync_api import Playwright

@pytest.fixture(scope="class")
def browser(playwright: Playwright):
    firefox = playwright.firefox
    browser_instance = firefox.launch()
    yield browser_instance
    browser_instance.close()

@pytest.fixture()
def page(browser):
    pw_page = browser.new_page()
    yield pw_page
