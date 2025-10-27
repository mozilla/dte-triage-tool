import streamlit as st
from datetime import datetime, timezone


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

    def display_project_suite_header(self):
        """
        Display the project and suite name in the header.
        """
        container = st.container(border=True, height="content", gap="small")
        form_values: FormValues = self.board_controller.state.get_form_values()
        container.markdown(f"**Project**: :blue-background[{form_values['project_name']}]")
        container.markdown(f"**Suite**: :blue-background[{form_values['suite_name']}]")
        form_values = self.form_controller.additional_search_params(container)
        if container.button("Filter Test Cases", key="filter-cases"):
            test_cases, msg = self.form_controller.query_and_save(form_values)
            if test_cases:
                self.board_controller.normalize_and_save_data(test_cases)
            else:
                st.warning(msg)

    def body(self):
        # Main content area
        if self.board_controller.state.has_initial_board():
            self.display_project_suite_header()
            self.display_kanban_board(self.board_controller.state.get_initial_board())
        else:
            st.info(
                "Please configure the triage settings in the sidebar and click 'Fetch Test Cases'."
            )

    def commit(self):
        """Commit the changes in the test cases to test rail."""
        st.sidebar.warning("Changes Detected")
        st.sidebar.button(
            "Commit Changes", on_click=self.show_changes, key="commit-button"
        )

    @st.dialog("Current Changes:", on_dismiss="rerun", width="large")
    def show_changes(self):
        """Dialog to show the changes in the status of the test cases."""
        formated_status_map = self.board_controller.format_status_map()
        st.table(formated_status_map)
        left, right = st.columns([0.3, 0.7], gap="small")
        submitted = left.button(
            "Submit",
            on_click=self.form_controller.commit_changes_to_testrail,
            key="submit-button",
        )
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H_%M_%SZ")
        right.download_button(
            use_container_width=True,
            label="Download Session Data(CSV)",
            data=self.convert_for_download(formated_status_map),
            file_name=f"session_{timestamp}.csv",
            mime="text/csv",
            icon=":material/download:",
        )
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

    @staticmethod
    def convert_for_download(df):
        return df.to_csv().encode("utf-8")
