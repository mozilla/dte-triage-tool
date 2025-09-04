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

    def set_inputs(self):
        """ Set the inputs for the form"""
        available_priorities = [(priority['id'], priority['name']) for priority in
                                self.triage.get_and_cache_priorities()]
        return {'project_id': st.text_input("Project ID", "17", key="project-id-input"),
                'suite_id': st.text_input("Suite ID", "2054", key="suite-id-input"),
                'priority_id': st.multiselect("Priority ID", available_priorities, key="priority-input"),
                'automation_status': st.multiselect("Automation Status", AUTOMATION_STATUSES, key="automation-status-input"),
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
            "priority_ids": Util.extract_and_concat_ids(form_values.get("priority_id")),
            "automation_status_ids": Util.extract_and_concat_ids(form_values.get("automation_status")),
            "limit": int(form_values.get("limit"))
        }
        try:
            test_cases = self.triage.fetch_test_cases(extracted_data)
            self.state.set_test_cases(test_cases)
            return True, "Success"
        except Exception as e:
            self.state.clear_test_cases()
            return False, str(e)
