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
        expander = st.expander("Priority and Automation Status")
        return {
            "project_id": st.text_input("Project ID", "17", key="project-id-input"),
            "project_name": "",
            "suite_id": st.text_input("Suite ID", "2054", key="suite-id-input"),
            "suite_name": "",
            "priority_id": expander.multiselect(
                "Priority ID",
                available_priorities,
                default=available_priorities,
                key="priority-input",
            ),
            "automation_status": expander.multiselect(
                "Automation Status",
                AUTOMATION_STATUSES,
                default=AUTOMATION_STATUSES,
                key="automation-status-input",
            ),
            "limit": st.text_input("Limit", 15),
        }

    def additional_search_params(self, container):
        """Additional search params to be passed to the testrail query"""
        search_params = self.state.get_search_params()
        expander = container.expander("Sections and Rotations")
        form_values = self.state.get_form_values()
        form_values |= {
            "section_id": expander.selectbox(
                "Section", search_params.get("sections"), key="sections-input", index=None
            ),
            "custom_rotation": expander.selectbox(
                "Rotations", search_params.get("rotations"), key="rotations-input", index=None
            ),
        }
        self.state.set_form_values(form_values)
        return form_values

    def query_and_save(self, form_values: dict) -> tuple[dict, str]:
        """
        Save the form data to the session state.
        """
        self.clear_on_fetch()
        required = ("project_id", "suite_id")
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
        additional_required = ("custom_rotation", "section_id")
        if all(k in form_values and form_values.get(k) for k in additional_required):
            extracted_data |= {
                "custom_rotation": form_values.get("custom_rotation"),
                "section_id": form_values.get("section_id")[0],
            }
        self.update_project_and_suite_names(form_values)
        self.state.set_form_values(form_values)
        if not self.state.has_search_params():
            self.triage.get_and_set_sections(
                extracted_data.get("project_id"), extracted_data.get("suite_id")
            )
        try:
            test_cases = self.triage.fetch_test_cases(extracted_data)
            return test_cases, "Success"
        except Exception as e:
            return {}, str(e)

    def update_project_and_suite_names(self, form_input: FormValues):
        """
        Sets the project and suite names in the form input based on their respective IDs.

        Args:
            form_input (FormValues): The form input data containing the project and suite IDs.
        """
        project = self.query_testrail_entry(
            int(form_input.get("project_id")), "project"
        )
        suite = self.query_testrail_entry(int(form_input.get("suite_id")), "suite")
        form_input["project_name"] = project.get("name")
        form_input["suite_name"] = suite.get("name")
        self.state.set_form_values(form_input)

    def query_testrail_entry(self, query_id: int, query_key: str):
        """
        Given an id and a query key, query a testrail entry. (currently project or suite)
        """
        query = {
            "project": self.triage.tr_session.get_project,
            "suite": self.triage.tr_session.get_suite,
            "case": self.triage.tr_session.get_case,
        }
        return query.get(query_key)(query_id)

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
