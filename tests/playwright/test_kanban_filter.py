from os import environ
import pytest
from time import sleep
from .locators import Locators

SUITE_ID = "37522"

@pytest.fixture()
def modify_env():
    environ["TESTRAIL_PROJECT_ID"] = "72"

def test_filter_cases(page, local_instance: str, locators: Locators):
    sleep(5)
    page.goto(local_instance, wait_until="domcontentloaded")

    locators.suite_id_input.clear()
    locators.suite_id_input.fill(SUITE_ID)
    locators.priority_input.click()
    page.get_by_text("Critical").click()
    locators.priority_chevron.click()
    locators.automation_status_input.click()
    page.get_by_text("Untriaged").click()
    locators.automation_status_chevron.click()

    locators.fetch_button.click()
