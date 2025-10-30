from playwright.sync_api import Page


class Locators:
    def __init__(self, page: Page):
        self.page = page

        # locators go here
        # sidebar and filter locators
        self.sidebar = self.page.locator(".stSidebar")
        self.filter_expander = self.page.locator(".stExpander")
        self.project_id_input = self.page.locator(".st-key-project-id-input input")
        self.suite_id_input = self.page.locator(".st-key-suite-id-input input")
        self.priority_input = self.page.locator(".st-key-priority-input input")
        self.priority_chevron = self.page.locator(
            ".st-key-priority-input svg[title='open']"
        )
        self.automation_status_input = self.page.locator(
            ".st-key-automation-status-input input"
        )
        self.automation_status_chevron = self.page.locator(
            ".st-key-automation-status-input svg[title='open']"
        )

        # additional filter container
        self.project_suite_name_container = self.page.locator(
            ".st-key-project-suite-name-container"
        )
        self.section_id_input = self.page.locator(".st-key-sections-input input")
        self.custom_rotation_input = self.page.locator(".st-key-rotations-input input")
        self.dropdown_element = self.page.get_by_test_id("stSelectboxVirtualDropdown")
        # alert containers
        self.alert_container = self.page.locator(
            ".stSidebar div[data-testid='stAlertContainer']"
        )

        # buttons
        self.fetch_button = self.page.locator(".st-key-fetch-button button")
        self.commit_button = self.page.locator(".st-key-commit-button button")

        # Droppable area
        self.kanban_board_frame = self.page.frame_locator(".stCustomComponentV1")
        self.status_untriaged = self.kanban_board_frame.locator(
            "div[data-rbd-droppable-id='status untriaged']"
        )
        self.status_suitable = self.kanban_board_frame.locator(
            "div[data-rbd-droppable-id='status suitable']"
        )
        self.status_unsuitable = self.kanban_board_frame.locator(
            "div[data-rbd-droppable-id='status unsuitable']"
        )
        self.status_completed = self.kanban_board_frame.locator(
            "div[data-rbd-droppable-id='status completed']"
        )
        self.status_disabled = self.kanban_board_frame.locator(
            "div[data-rbd-droppable-id='status disabled']"
        )
