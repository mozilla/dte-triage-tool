from collections import defaultdict

import streamlit as st

from src.core.controllers.base_controller import BaseController
from src.core.triage import Triage
from src.config.types import FormValues
from src.core.util import Util

AUTOMATION_STATUSES = [
    (1, "Untriaged"),
    (2, "Suitable"),
    (3, "Unsuitable"),
    (4, "Completed"),
    (5, "Disabled"),
]


class TriageFormController(BaseController):
    def __init__(self, state=None):
        super().__init__(state)
        self.triage = Triage().get_instance()
        self.inverted_status_translation = {
            v.lower(): k for k, v in self.status_translation.items()
        }

    def set_inputs(self):
        """Set the inputs for the form"""
        available_priorities = [
            (priority["id"], priority["name"])
            for priority in self.triage.get_and_cache_priorities()
        ]
        return {
            "project_id": st.text_input("Project ID", "17", key="project-id-input"),
            "suite_id": st.text_input("Suite ID", "68103", key="suite-id-input"),
            "priority_id": st.multiselect(
                "Priority ID",
                available_priorities,
                default=available_priorities,
                key="priority-input",
            ),
            "automation_status": st.multiselect(
                "Automation Status",
                AUTOMATION_STATUSES,
                default=AUTOMATION_STATUSES,
                key="automation-status-input",
            ),
            "limit": st.text_input("Limit", 15),
        }

    def query_and_save(self, form_values: FormValues) -> tuple[dict, str]:
        """
        Save the form data to the session state.
        """
        self.clear_on_fetch()
        self.state.set_form_values(form_values)
        required = ("project_id", "suite_id", "priority_id", "automation_status")
        if not all(k in form_values and form_values.get(k) for k in required):
            return {}, "Please fill in all required fields."
        extracted_data = {
            "project_id": int(form_values.get("project_id")),
            "suite_id": int(form_values.get("suite_id")),
            "priority_id": Util.extract_and_concat_ids(form_values.get("priority_id")),
            "custom_automation_status": Util.extract_and_concat_ids(
                form_values.get("automation_status")
            ),
            "limit": int(form_values.get("limit")),
        }
        try:
            test_cases = self.triage.fetch_test_cases(extracted_data)
            return test_cases, "Success"
        except Exception as e:
            return {}, str(e)

    def commit_changes_to_testrail(self):
        """Commit the changes in the test cases to test rail."""
        status_map = self.state.get_status_map()
        grouped_tc = defaultdict(list)
        for tc_id, status_change in status_map.items():
            _, current_status = status_change
            status_code = self.inverted_status_translation.get(current_status)
            grouped_tc[status_code].append(tc_id)
        return self.triage.update_case_automation_statuses(grouped_tc)

    def clear_on_fetch(self):
        """Clear the form values and initial board data."""
        self.state.clear_initial_board()
        self.state.clear_status_map()
        self.state.clear_form_values()
