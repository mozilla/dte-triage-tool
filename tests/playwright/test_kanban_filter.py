from .locators import Locators
from playwright.sync_api import expect

INCORRECT_GRAVEYARD_PRJ_ID = "72"


def test_kanban_filter_handle_error(
    search_data, page, local_instance: str, locators: Locators
):
    page.goto(local_instance, wait_until="domcontentloaded")
    locators.filter_expander.click()

    locators.project_id_input.clear()
    # incorrect project id
    locators.project_id_input.fill(INCORRECT_GRAVEYARD_PRJ_ID)

    locators.suite_id_input.clear()
    locators.suite_id_input.fill(search_data["suite_id"])

    locators.fetch_button.click()
    expect(locators.alert_container).to_be_visible()
    expect(locators.alert_container).to_contain_text("TestRail API returned HTTP 400")


def test_project_search_and_filter(
    input_search_params, search_data, page, local_instance: str, locators: Locators
):
    expect(locators.project_suite_name_container).to_be_visible()
    project_container = locators.project_suite_name_container.get_by_text("Project:")
    suite_container = locators.project_suite_name_container.get_by_text("Suit`e:")
    # click expander
    expander = locators.project_suite_name_container.get_by_test_id("stExpander")
    expander.click()
    # get section filter and rotation filter
    section_filter = locators.section_id_input
    rotation_filter = locators.custom_rotation_input
    expect(project_container).to_contain_text(search_data["project_name"])
    expect(suite_container).to_contain_text(search_data["suite_name"])
    expect(section_filter).to_be_visible()
    section_filter.click()
    expect(locators.dropdown_element).to_be_visible()
    page.keyboard.press("Escape")
    expect(rotation_filter).to_be_visible()
