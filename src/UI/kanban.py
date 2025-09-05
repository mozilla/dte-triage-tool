import streamlit as st

from streamlit_kanban import kanban

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
        st.markdown("This tool helps Desktop Test Engineering triage test cases for future automation.")

    def sidebar(self):
        with st.sidebar:
            st.header("Triage Configuration")
            form_values: FormValues = self.form_controller.set_inputs()
            if st.button("Fetch Test Cases"):
                test_cases, msg = self.form_controller.query_and_save(form_values)
                if test_cases:
                    self.board_controller.normalize_and_save_data(test_cases)
                    st.success("Test cases fetched.")
                else:
                    st.warning(msg)
            if self.board_controller.state.has_board():
                st.divider()
                st.button("Commit Changes.", on_click=self.submit_changes)


    def body(self):
        # Main content area
        if self.board_controller.state.has_board():
            self.display_kanban_board(self.board_controller.state.get_board())
        else:
            st.info("Please configure the triage settings in the sidebar and click 'Fetch Test Cases'.")

    @st.dialog("Commit Changes")
    def submit_changes(self):
        # changed_cases = self.board_controller.map_status_transitions()
        st.warning("No changes found.")

    def display_kanban_board(self, test_cases):
        """
            Displays the Kanban board with the fetched test cases.
        """
        if test_cases:
            changed_board = kanban(test_cases, f"board_{len(test_cases)}")
            if changed_board:
                self.board_controller.update_board(changed_board)
            else:
                self.board_controller.update_board(test_cases)
        else:
            st.info("No test cases found.\nChange search criteria and retry.")

    def run(self):
        self.header()
        self.sidebar()
        self.body()
