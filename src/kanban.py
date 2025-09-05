import streamlit as st

from streamlit_kanban import kanban

from src.core.intergrations.controllers.triage_form import TriageFormController
from src.core.util import Util
from src.config.types import FormValues

class Kanban:
    def __init__(self):
        st.set_page_config(layout="wide")
        self.form_controller = TriageFormController()

    @staticmethod
    def header():
        st.title("Test Case Triage Kanban Board")
        st.markdown("This tool helps Desktop Test Engineering triage test cases for future automation.")

    def body(self):
        with st.sidebar:
            st.header("Triage Configuration")
            form_values: FormValues = self.form_controller.set_inputs()
            if st.button("Fetch Test Cases"):
                ok, msg = self.form_controller.query_and_save(form_values)
                if not ok:
                    st.warning(msg)
                else:

                    st.success("Test cases fetched.")
        # Main content area
        if self.form_controller.state.has_test_cases():
            self.display_kanban_board(self.form_controller.state.get_test_cases())
        else:
            st.info("Please configure the triage settings in the sidebar and click 'Fetch Test Cases'.")

    def display_kanban_board(self, test_cases):
        """
            Displays the Kanban board with the fetched test cases.
        """
        if test_cases:
            kanban(test_cases, f"kanban_board")
        else:
            st.info("No test cases found.\nChange search criteria and retry.")


    def run(self):
        print("Running Kanban")
        self.header()
        self.body()
