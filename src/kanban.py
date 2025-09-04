import streamlit as st

from streamlit_kanban import kanban

from src.core.integrations.controllers.triage_form import TriageFormController
from src.core.util import Util
from src.config.types import FormValues

AUTOMATION_STATUSES = [
    "Status_Untriaged",
    "Status_Suitable",
    "Status_Unsuitable",
    "Status_Completed",
    "Status_Disabled",
]


class Kanban:
    def __init__(self):
        st.set_page_config(layout="wide")
        self.form_controller = TriageFormController()
        self.status_translation = {
            1: "Status_Untriaged",
            2: "Status_Suitable",
            3: "Status_Unsuitable",
            4: "Status_Completed",
            5: "Status_Disabled",
        }
        self.priority_translation = {
            1: "Priority Low",
            2: "Priority Medium",
            3: "Priority High",
            4: "Priority Critical",
        }

    @staticmethod
    def header():
        st.title("Test Case Triage Kanban Board")
        st.markdown(
            "This tool helps Desktop Test Engineering triage test cases for future automation."
        )

    def body(self):
        with st.sidebar:
            st.header("Triage Configuration")
            form_values: FormValues = self.form_controller.set_inputs()
            if st.button("Fetch Test Cases", key="fetch-button"):
                ok, msg = self.form_controller.query_and_save(form_values)
                if not ok:
                    st.warning(msg)
                else:
                    st.success("Test cases fetched.")
        # Main content area
        if self.form_controller.state.has_test_cases():
            self.display_kanban_board(self.form_controller.state.get_test_cases())
        else:
            st.info(
                "Please configure the triage settings in the sidebar and click 'Fetch Test Cases'."
            )

    def display_kanban_board(self, test_cases):
        """
        Displays the Kanban board with the fetched test cases.
        """
        if test_cases:
            test_cases = test_cases.get("cases", [])
            cols = {
                status: {"id": status.lower(), "title": status, "cards": []}
                for status in self.status_translation.values()
            }
            for test_case in test_cases:
                case_automation_status = self.status_translation[
                    test_case["custom_automation_status"]
                ]
                cols[case_automation_status]["cards"].append(
                    {
                        "id": f"card-{test_case['id']}",
                        "name": test_case["title"],
                        "fields": [
                            f"{self.priority_translation[test_case['priority_id']]}"
                        ],
                        "color": Util.priority_color(test_case["priority_id"]),
                    }
                )
            kanban(list(cols.values()), f"test_cases_{len(test_cases)}")
        else:
            st.info("No test cases found.\nChange search criteria and retry.")

    def run(self):
        self.header()
        self.body()
