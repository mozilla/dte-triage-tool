from os import environ
import pytest
from .locators import Locators

GRAVEYARD_PRJ = "72"
SUITE_ID = "37522"


@pytest.fixture()
def modify_env():
    environ["TESTRAIL_PROJECT_ID"] = GRAVEYARD_PRJ


def test_filter_cases(page, local_instance: str, locators: Locators):
    page.goto(local_instance, wait_until="domcontentloaded")

    locators.filter_expander.click()

    locators.project_id_input.clear()
    locators.project_id_input.fill(GRAVEYARD_PRJ)

    locators.suite_id_input.clear()
    locators.suite_id_input.fill(SUITE_ID)
    locators.priority_input.click()
    page.get_by_text("Critical").click()
    locators.priority_chevron.click()
    locators.automation_status_input.click()
    page.get_by_text("Untriaged").click()
    locators.automation_status_chevron.click()

    locators.fetch_button.click()