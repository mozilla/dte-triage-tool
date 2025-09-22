from src.core.integrations.testrail_integration import TestRail
from src.core.integrations.bugzilla_integration import Bugzilla
from src.core.state import SessionState
from src.config.setting import Settings
from src.config.types import Priority, FormValues

FUNCTIONAL_ROOT_METABUG = 1976270

class Triage:
    """
    Class used to interact with the TestRail & Bugzilla API integrations.
    Singleton Class.
    """

    _instance = None

    def __init__(self, state=None):
        local = Settings.testrail_base_url.split("/")[2].startswith("127")
        # TODO: standardize how we're getting API keys
        self.tr_session = TestRail(
            Settings.testrail_base_url,
            Settings.testrail_username,
            Settings.testrail_api_key,
            local,
        )
        self.bz_session = Bugzilla(
            Settings.bugzilla_base_url
        )
        self.state = state if state else SessionState()

    def __new__(cls, state=None):
        """New Instance of Triage Class if not already created."""
        if cls._instance is None:
            cls._instance = super(Triage, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        """
        Returns the instance of Triage Class.
        """
        return cls._instance or cls()

    def fetch_test_cases(self, extracted_data: FormValues):
        """
        Fetches test cases from TestRail based on the provided criteria.
        """
        return self.tr_session.get_test_cases(extracted_data)

    def get_and_cache_priorities(self):
        """query priorities if data is not cached. get cached value if available."""
        if self.state.has_priorities():
            return self.state.get_priorities()
        available_priorities: list[Priority] = self.tr_session.get_priorities()
        self.state.set_priorities(available_priorities)
        return available_priorities

    def update_case_automation_statuses(self, formated_data: dict[str, list[int]]):
        """update the automation status of the test cases."""
        suite_id = self.state.get_form_values().get("suite_id")
        for status_code, test_cases in formated_data.items():
            payload = {
                "case_ids": test_cases,
                "custom_automation_status": status_code,
            }
            self.tr_session.update_test_cases(payload, suite_id)
            bz_content_payload = self.tr_session.get_bugzilla_content(payload, suite_id)
            self.bz_session.create_bug_structure(FUNCTIONAL_ROOT_METABUG, bz_content_payload)
