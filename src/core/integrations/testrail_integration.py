from typing import Optional

from src.config.types import FormValues
from src.core.integrations.api import TestRailAPIClient

CASE_VIEW_URL = "index.php?/cases/view"


class TestRail:
    """
    Object describing all necessary API endpoints (and related data handling
    methods) for test result reporting.

    Attributes:
    ===========

    host: str
      The "home" of the TestRail instance in question

    username: str
      The username of the TestRail user

    password: str
      The API key of the user in question

    local: bool
      Assign True if the instance of TestRail is hosted on localhost
    """

    def __init__(self, host, username, password, local=False):
        self.client = TestRailAPIClient(host, local)
        self.client.user = username
        self.client.password = password

    # Public Methods

    def get_test_case(self, case_id):
        """
        Given a case_id, get the cooresponding test case.

        :param case_id: case_id
        :return: a test case
        """
        return self.client.send_get(f"get_case/{case_id}")

    def get_test_cases(self, query_params: Optional[FormValues]):
        """
        Get test cases associated with a specific project (and optional filters).

        :param query_params: Optional dictionary of filter key-value pairs.
        :return: List of test cases matching the filters.
        """
        project_id = query_params.pop("project_id")
        query_string = "&".join(f"{key}={val}" for key, val in query_params.items())
        endpoint = (
            f"get_cases/{project_id}&{query_string}"
            if query_params
            else f"get_cases/{project_id}"
        )
        return self.client.send_get(endpoint)

    def get_priorities(self):
        """Get available priorities."""
        return self.client.send_get("get_priorities")

    def get_case_fields(self):
        """Get available case fields."""
        return self.client.send_get("get_case_fields")

    def update_test_cases(self, payload, suite_id):
        """update the test cases of the given suite id with the given payload."""
        return self.client.send_post(f"update_cases/{suite_id}", payload)

    def get_suite(self, suite_id):
        """Return the suite object"""
        return self.client.send_get(f"get_suite/{suite_id}")

    def get_case(self, case_id):
        """Return the test case object"""
        return self.client.send_get(f"get_case/{case_id}")

    def get_bugzilla_content(self, payload, suite_id):
        """
        Given a payload for updating cases and a suite id, get necessary content
        to create a suite metabug and testcase automation bugs
        """
        if payload.get("custom_automation_status") != 2:
            return {}
        bugzilla_content = {
            "suite_id": suite_id,
        }
        suite = self.get_suite(suite_id)
        bugzilla_content["suite_name"] = suite.get("name")
        bugzilla_content["cases"] = []
        for case_id in payload.get("case_ids"):
            case_ = self.get_case(case_id)
            test_loc = case_.get("custom_automation_test_names")
            if not test_loc or "/" not in test_loc:
                repo_dir = None
            else:
                repo_dir = test_loc.split("/")[1]
            test_steps = ""
            description = case_.get("title")
            if case_.get("custom_preconds"):
                test_steps = test_steps + case_["custom_preconds"] + "\n\n"
            if case_.get("custom_steps"):
                test_steps = test_steps + case_["custom_steps"] + "\n\n"
            if case_.get("custom_steps_separated"):
                for step in case_["custom_steps_separated"]:
                    if step.get("content"):
                        test_steps = test_steps + step["content"] + "\n"
            case_link = "/".join(
                [self.client.get_base_url(), CASE_VIEW_URL, str(case_id)]
            )
            bugzilla_content["cases"].append(
                {
                    "case_description": description,
                    "case_id": case_id,
                    "repo_dir": repo_dir,
                    "test_steps": test_steps,
                    "case_link": case_link,
                }
            )
        return bugzilla_content
