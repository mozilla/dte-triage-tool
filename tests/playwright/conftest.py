import pytest
from os import environ
from subprocess import Popen
from playwright.sync_api import Playwright
from .locators import Locators

APP_TITLE = "Streamlit"

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

@pytest.fixture()
def local_instance(modify_env):
    port = environ.get("STREAMLIT_PORT") or 8501
    command = f"streamlit run main.py --server.port {port} --server.headless true"
    proc = Popen(command.split(" "))
    yield f"http://localhost:{port}"
    proc.kill()

@pytest.fixture()
def locators(page):
    return Locators(page)
