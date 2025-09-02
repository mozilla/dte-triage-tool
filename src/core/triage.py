from src.core.intergrations.testrail_integration import TestRail
from src.core.state import SessionState
from src.config.setting import Settings
from src.core.types import Priority


class Triage:
    """
        Class used to interact with the TestRail & Bugzilla API integrations.
        Singleton Class.
    """
    _instance = None
    def __init__(self, state=None):
        local = Settings.testrail_base_url.split("/")[2].startswith("127")
        self.tr_session = TestRail(
        Settings.testrail_base_url,
        Settings.testrail_username,
        Settings.testrail_api_key,
        local,
    )
        self.state = state if state else SessionState()

    def __new__(cls):
        """ New Instance of Triage Class if not already created."""
        if cls._instance is None:
            cls._instance = super(Triage, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        """ Returns the instance of Triage Class."""
        return cls._instance or cls()

    def fetch_test_cases(self, suite_id, priority_ids, automation_status_ids):
        """
        Fetches test cases from TestRail based on the provided criteria.
        """
        form_values = {
            "suite_id": int(suite_id),
            "priority_id": priority_ids,
            "automation_status": automation_status_ids
        }
        return self.tr_session.get_test_cases(17, form_values)

    def get_and_cache_priorities(self):
        """ query priorities if data is not cached. get cached value if available. """
        if self.state.has_priorities():
            return self.state.get_priorities()
        available_priorities: list[Priority] = self.tr_session.get_priorities()
        self.state.set_priorities(available_priorities)
        return available_priorities