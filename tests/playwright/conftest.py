import pytest
import subprocess as sp
from time import sleep
from os import environ
from playwright.sync_api import Playwright
from .locators import Locators
import urllib3

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
    proc = sp.Popen(command.split(" "))
    ping_success = False
    host = f"http://localhost:{port}"
    while not ping_success:
        try:
            ping_success = 199 < urllib3.request("GET", host).status < 300
        except urllib3.exceptions.MaxRetryError:
            ping_success = False
        sleep(0.5)

    yield host
    proc.kill()


@pytest.fixture()
def locators(page):
    return Locators(page)
