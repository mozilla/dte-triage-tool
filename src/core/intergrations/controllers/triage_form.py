import streamlit as st

from src.core.state import SessionState
from src.core.triage import Triage
from src.config.types import FormValues
from src.core.util import Util

AUTOMATION_STATUSES = [(1, 'Untriaged'), (2, 'Suitable'), (3, 'Unsuitable'), (4, 'Completed'), (5, 'Disabled')]


class TriageFormController:

    def __init__(self, state=None):
        self.triage = Triage().get_instance()
        self.state = state if state else SessionState()
        self.status_translation = {
            1: "Status_Untriaged",
            2: "Status_Suitable",
            3: "Status_Unsuitable",
            4: "Status_Completed",
            5: "Status_Disabled"
        }
        self.priority_translation = {
            1: "Priority Low",
            2: "Priority Medium",
            3: "Priority High",
            4: "Priority Critical"
        }

    def set_inputs(self):
        """ Set the inputs for the form"""
        available_priorities = [(priority['id'], priority['name']) for priority in
                                self.triage.get_and_cache_priorities()]
        return {'project_id': st.text_input("Project ID", "17"),
                'suite_id': st.text_input("Suite ID", "2054"),
                'priority_id': st.multiselect("Priority ID", available_priorities),
                'automation_status': st.multiselect("Automation Status", AUTOMATION_STATUSES),
                'limit': st.text_input("Limit", 100)}

    def query_and_save(self, form_values: FormValues) -> tuple[bool, str]:
        """
            Save the form data to the session state.
        """
        required = ("project_id", "suite_id", "priority_id", "automation_status")
        self.state.clear_test_cases()
        if not all(k in form_values and form_values.get(k) for k in required):
            return False, "Please fill in all required fields."
        extracted_data = {
            "project_id": int(form_values.get("project_id")),
            "suite_id": int(form_values.get("suite_id")),
            "priority_id": Util.extract_and_concat_ids(form_values.get("priority_id")),
            "custom_automation_status": Util.extract_and_concat_ids(form_values.get("automation_status")),
            "limit": int(form_values.get("limit", ))
        }
        try:
            test_cases = self.triage.fetch_test_cases(extracted_data)
            self.state.set_test_cases(test_cases)
            return True, "Success"
        except Exception as e:
            self.state.clear_test_cases()
            return False, str(e)

    def normalize_and_format_data(self, test_cases: dict[str, list[dict] | dict]):
        """ Takes the test case data and formats it for the kanban board view. """
        test_cases = test_cases.get('cases', [])
        cols = {
            status: {
                "id": status.lower(),
                "title": status,
                "cards": []
            } for status in self.status_translation.values()
        }
        for test_case in test_cases:
            case_automation_status = self.status_translation[test_case['custom_automation_status']]
            cols[case_automation_status]['cards'].append(
                {"id": f"card-{test_case['id']}", "name": test_case['title'],
                 "fields": [f"{self.priority_translation[test_case['priority_id']]}",
                            f"Test Case ID: {test_case['id']}"],
                 "color": Util.priority_color(test_case['priority_id'])})
        return list(cols.values())
