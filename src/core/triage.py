from src.core.integrations.testrail_integration import TestRail
from src.core.integrations.bugzilla_integration import Bugzilla
from src.core.state import SessionState
from src.config.setting import Settings
from src.core.util import Util
from src.config.types import Priority, FormValues
import json
from datetime import datetime

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
        self.bz_session = Bugzilla(Settings.bugzilla_base_url)
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
        return self.tr_session.get_cases(extracted_data)

    def get_and_cache_priorities(self):
        """query priorities if data is not cached. get cached value if available."""
        if self.state.has_priorities():
            return self.state.get_priorities()
        available_priorities: list[Priority] = self.tr_session.get_priorities()
        self.state.set_priorities(available_priorities)
        return available_priorities

    def get_and_set_sections(self, project_id: str, suite_id: str):
        """Query and save the sections of the given project and suite."""
        sections = self.tr_session.get_sections(project_id, suite_id).get(
            "sections", []
        )
        filtered_sections = Util.extract_section_name_and_ids(sections)
        if filtered_sections:
            self.state.set_search_params("sections", filtered_sections)
        return filtered_sections

    def update_case_automation_statuses(self, formated_data: dict[int, list[int]]):
        """update the automation status of the test cases."""
        suite_id = self.state.get_form_values().get("suite_id")
        bz_content_payload = {}
        for status_code, test_cases in formated_data.items():
            payload = {
                "case_ids": test_cases,
                "custom_automation_status": status_code,
            }
            self.tr_session.update_test_cases(payload, suite_id)
            if status_code == 2:
                initial_suitable_case_ids = Util.extract_case_ids_from_board(
                    2, self.state.get_initial_board()
                )
                valid_suitable_case_ids = list(
                    filter(
                        lambda case_id: case_id not in initial_suitable_case_ids,
                        test_cases,
                    )
                )
                if not self.bz_session.find_bugs_by_test_case_ids(
                    valid_suitable_case_ids
                ):
                    payload["case_ids"] = valid_suitable_case_ids
                bz_content_payload |= self.tr_session.get_bugzilla_content(
                    payload, suite_id
                )
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H_%M_%SZ")
        with open(f"session_{timestamp}.json", "w") as fh:
            json.dump(bz_content_payload, fh, indent=2)
        # TODO: Eventually, need to consider re-enabling this
        # self.bz_session.create_bug_structure(FUNCTIONAL_ROOT_METABUG, bz_content_payload)
