from os import environ
import pytest

from .conftest import locators
from .locators import Locators
from playwright.sync_api import expect

def test_commit_button_appear_on_assign(input_search_params, search_data, page, local_instance: str, locators: Locators):
    test_case = locators.kanban_board_frame.get_by_test_id(search_data["test_case_id"])
    status_untriaged_container = locators.status_untriaged
    status_suitable_container = locators.status_suitable
    test_case.drag_to(status_suitable_container)
    test_case.click()



