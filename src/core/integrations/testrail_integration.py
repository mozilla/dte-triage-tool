from typing import Optional

from src.config.types import FormValues
from src.core.integrations.api import APIClient



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
        self.client = APIClient(host, local)
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
