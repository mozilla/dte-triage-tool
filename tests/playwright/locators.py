from playwright.sync_api import Page

class Locators:
    def __init__(self, page: Page):
        self.page = page

        #locators go here
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

        self.fetch_button = self.page.locator(".st-key-fetch-button button")
