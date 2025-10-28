import pytest
from src.core.controllers.form_controller import FormController
from unittest.mock import MagicMock, patch


@pytest.fixture
def controller(session_state):
    return FormController(state=session_state)


class TestFormController:
    @patch("streamlit.text_input")
    @patch("streamlit.expander")
    def test_set_inputs_returns_form_structure(
        self, mock_expander, mock_text_input, controller
    ):
        """Test that set_inputs returns the correct form structure"""
        mock_priorities = [
            {"id": 1, "name": "High"},
            {"id": 2, "name": "Medium"},
            {"id": 3, "name": "Low"},
        ]
        controller.state.set_priorities(mock_priorities)

        # Mock streamlit components
        mock_text_input.return_value = "id_values"
        mock_expander_instance = MagicMock()
        mock_expander.return_value = mock_expander_instance
        mock_expander_instance.multiselect.return_value = []

        result = controller.set_inputs()
        input_keys = [
            "project_id",
            "suite_id",
            "priority_id",
            "automation_status",
            "limit",
            "project_name",
            "suite_name",
        ]
        for key in input_keys:
            assert key in result

    def test_query_and_save_missing_required_fields(self, controller):
        """Test that query_and_save returns error message when required fields are missing"""

        missing_key_form = {
            "project_id": "17",
            "priority_id": [(1, "High")],
            "automation_status": [(1, "Untriaged")],
        }
        empty_value_form = {
            "project_id": "",
            "suite_id": "2054",
            "priority_id": [(1, "High")],
            "automation_status": [(1, "Untriaged")],
        }
        result, message = controller.query_and_save(missing_key_form)

        assert result == {}
        assert message == "Please fill in all required fields."

        result, message = controller.query_and_save(empty_value_form)

        assert result == {}
        assert message == "Please fill in all required fields."

    def test_query_and_save_success(self, controller):
        """Test successful query_and_save with all required fields"""
        form_values = {
            "project_id": "17",
            "suite_id": "2054",
            "priority_id": [(1, "High"), (2, "Medium")],
            "automation_status": [(1, "Untriaged"), (2, "Suitable")],
            "limit": "15",
        }

        # Mock the necessary methods
        mock_test_cases = {
            "cases": [{"id": 1, "title": "Test Case", "custom_automation_status": 2}]
        }
        controller.triage.fetch_test_cases = MagicMock(return_value=mock_test_cases)
        controller.update_project_and_suite_names = MagicMock()

        result, message = controller.query_and_save(form_values)

        assert result == mock_test_cases
        assert controller.update_project_and_suite_names.called

    def test_query_and_save_handles_exceptions(self, controller):
        """Test that query_and_save properly handles exceptions"""
        form_values = {
            "project_id": "17",
            "suite_id": "2054",
            "priority_id": [(1, "High")],
            "automation_status": [(1, "Untriaged")],
            "limit": "15",
        }

        controller.triage.fetch_test_cases = MagicMock(
            side_effect=Exception("Connection error")
        )
        controller.update_project_and_suite_names = MagicMock()

        result, message = controller.query_and_save(form_values)

        assert result == {}
        assert message == "Connection error"

    def test_update_project_and_suite_names(self, controller):
        """Test that project and suite names are properly updated"""
        form_input = {"project_id": "17", "suite_id": "2054"}

        mock_project = {"id": 17, "name": "Test Project"}
        mock_suite = {"id": 2054, "name": "Test Suite"}

        controller.query_testrail_entry = MagicMock(
            side_effect=[mock_project, mock_suite]
        )
        controller.update_project_and_suite_names(form_input)

        assert form_input["project_name"] == "Test Project"
        assert form_input["suite_name"] == "Test Suite"

        assert controller.state.get_form_values()["project_name"] == "Test Project"
        assert controller.state.get_form_values()["suite_name"] == "Test Suite"

    def test_query_testrail_entry(self, controller):
        """Test querying a project from TestRail"""
        mock_project = {"id": 17, "name": "Test Project"}
        mock_suite = {"id": 2054, "name": "Test Suite"}
        mock_case = {"id": 123, "title": "Test Case"}
        controller.triage.tr_session.get_case = MagicMock(return_value=mock_case)
        controller.triage.tr_session.get_project = MagicMock(return_value=mock_project)
        controller.triage.tr_session.get_suite = MagicMock(return_value=mock_suite)

        assert controller.query_testrail_entry(17, "project") == mock_project
        controller.triage.tr_session.get_project.assert_called_once_with(17)

        assert controller.query_testrail_entry(2054, "suite") == mock_suite
        controller.triage.tr_session.get_suite.assert_called_once_with(2054)

        assert controller.query_testrail_entry(123, "case") == mock_case
        controller.triage.tr_session.get_case.assert_called_once_with(123)

    @patch("src.core.triage.Triage.update_case_automation_statuses")
    def test_commit_changes_to_testrail(self, update_case_automation_mock, controller):
        """Test committing changes to TestRail"""

        status_map = {
            1: ("status untriaged", "status suitable"),
            2: ("status suitable", "status completed"),
            3: ("status untriaged", "status completed"),
            4: ("status completed", "status disabled"),
        }
        grouped_tc = {2: [1], 4: [2, 3], 5: [4]}
        controller.state.set_status_map(status_map)

        controller.commit_changes_to_testrail()

        # Verify the method was called with grouped test cases
        update_case_automation_mock.assert_called_once()
        update_case_automation_mock.assert_called_with(grouped_tc)

    def test_clear_on_fetch(self, controller):
        """Test that clear_on_fetch clears all relevant state"""
        controller.state.set_initial_board([{"title": "Board"}])
        controller.state.set_status_map({1: ("Status Untriaged", "Status Suitable")})
        controller.state.set_form_values(
            {"suite_id": 12, "priority_id": 2, "automation_status": 3}
        )

        controller.clear_on_fetch()

        assert not controller.state.get_initial_board()
        assert not controller.state.get_status_map()
        assert not controller.state.get_form_values()
