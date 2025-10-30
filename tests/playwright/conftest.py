import pytest
import subprocess as sp
from time import sleep
from os import environ
from playwright.sync_api import Playwright
from .locators import Locators
import urllib3

APP_TITLE = "Streamlit"
GRAVEYARD_PROJECT_ID = "73"
SUITE_ID = "37522"


@pytest.fixture(scope="class")
def browser(playwright: Playwright):
    firefox = playwright.firefox
    browser_instance = firefox.launch(headless=False)
    yield browser_instance
    browser_instance.close()


@pytest.fixture()
def page(browser):
    pw_page = browser.new_page()
    yield pw_page


@pytest.fixture()
def modify_env():
    environ["TESTRAIL_PROJECT_ID"] = GRAVEYARD_PROJECT_ID


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


@pytest.fixture()
def search_data():
    return {
        "project_id": GRAVEYARD_PROJECT_ID,
        "suite_id": SUITE_ID,
        "project_name": "Project: Firefox Desktop - Graveyard",
        "suite_name": "Suite: [Fx106+] [QA-1544] PDF editing",
        "priority": "Critical",
        "test_case_id": "1855744",
        "automation_status": "Untriaged",
    }


@pytest.fixture()
def input_search_params(search_data, page, locators: Locators, local_instance: str):
    page.goto(local_instance, wait_until="domcontentloaded")

    locators.filter_expander.click()

    locators.project_id_input.clear()
    locators.project_id_input.fill(search_data["project_id"])

    locators.suite_id_input.clear()
    locators.suite_id_input.fill(search_data["suite_id"])

    locators.priority_input.click()
    page.get_by_text("Critical").click()

    locators.priority_chevron.click()
    locators.automation_status_input.click()
    page.get_by_text("Untriaged").click()

    locators.automation_status_chevron.click()

    locators.fetch_button.click()
