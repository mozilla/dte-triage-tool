import streamlit as st

from src.UI import kanban

from src.core.controllers.board_controller import BoardController
from src.core.controllers.form_controller import TriageFormController
from src.config.types import FormValues


class Kanban:
    def __init__(self):
        st.set_page_config(layout="wide")
        self.form_controller = TriageFormController()
        self.board_controller = BoardController()

    @staticmethod
    def header():
        st.title("Test Case Triage Kanban Board")
        st.markdown(
            "This tool helps Desktop Test Engineering triage test cases for future automation."
        )

    def sidebar(self):
        with st.sidebar:
            st.header("Triage Configuration")
            form_values: FormValues = self.form_controller.set_inputs()
            if st.button("Fetch Test Cases", key="fetch-button"):
                test_cases, msg = self.form_controller.query_and_save(form_values)
                if test_cases:
                    self.board_controller.normalize_and_save_data(test_cases)
                else:
                    st.warning(msg)

    def body(self):
        # Main content area
        if self.board_controller.state.has_initial_board():
            self.display_kanban_board(self.board_controller.state.get_initial_board())
        else:
            st.info(
                "Please configure the triage settings in the sidebar and click 'Fetch Test Cases'."
            )

    def commit(self):
        """ Commit the changes in the test cases to test rail. """
        st.sidebar.warning("Changes Detected")
        st.sidebar.button("Commit Changes", on_click=self.show_changes, key="commit-button")

    @st.dialog("Current Changes:", on_dismiss="rerun")
    def show_changes(self):
        """ Dialog to show the changes in the status of the test cases."""
        formated_status_map = self.board_controller.format_status_map()
        st.table(formated_status_map)
        submitted = st.button("Submit to TestRail", on_click=self.form_controller.commit_changes_to_testrail, key="submit-button")
        if submitted:
            self.form_controller.clear_on_fetch()
            st.rerun(scope="app")

    def display_kanban_board(self, test_cases):
        """
        Displays the Kanban board with the fetched test cases.
        """
        if test_cases:
            updated_cases = kanban(test_cases, str(test_cases))
            if updated_cases:
                self.board_controller.update_status_map(updated_cases[0])
        else:
            st.info("No test cases found.\nChange search criteria and retry.")

    def run(self):
        self.header()
        self.sidebar()
        self.body()
        if self.board_controller.state.has_status_map():
            self.commit()
