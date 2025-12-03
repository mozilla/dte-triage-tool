import pytest
from src.core.controllers.board_controller import BoardController
from src.core.util import Util
from pandas import DataFrame


@pytest.fixture
def controller(session_state):
    return BoardController(state=session_state)


class TestBoardController:
    def test_update_status_map_clears_then_sets(self, session_state, controller):
        controller.update_status_map({1: ("Status Untriaged", "Status Suitable")})

        assert session_state.get_status_map() == {
            1: ("Status Untriaged", "Status Suitable")
        }

    def test_status_map_headers_after_format(self, session_state, controller):
        session_state.set_status_map(
            {
                10: ("Status Untriaged", "Status Suitable"),
                20: ("Status Suitable", "Status Completed"),
            }
        )
        mock_test_cases = {"2": "status untriaged", "10": "status suitable"}
        df = controller.format_status_map(mock_test_cases)
        # check that the headers are set correctly
        assert list(df.columns) == controller.csv_headers

    def test_format_status_map_returns_proper_dataframe(
        self, session_state, controller
    ):
        # Set up test data
        status_map = {
            "1": ("Status Untriaged", "Status Suitable"),
            "2": ("Status Untriaged", "Status Completed"),
            "3": ("Status Completed", "Status Disabled"),
        }
        form_values = {"project_id": "P123", "suite_id": "S456"}

        session_state.set_status_map(status_map)
        session_state.set_form_values(form_values)
        mock_test_cases = {
            "1": "Status Untriaged",
            "2": "Status Untriaged",
            "3": "Status Completed",
        }

        # Get dataframe
        df: DataFrame = controller.format_status_map(mock_test_cases)

        assert len(df) == 3
        # check that the headers are set correctly and values are correct
        for col in df.iloc:
            cur = col.to_dict()
            assert all(el in controller.csv_headers for el in cur.keys())
            assert (cur["Original Status"], cur["Current Status"]) == status_map[
                cur["Test Case ID"]
            ]

    def test_normalize_and_save_data_builds_board_and_saves(
        self, session_state, controller
    ):
        """
        The controller must:
        - Create columns for each status in BaseController.status_translation
        - Append cards per case with translated priority label and color
        - Save to session state's initial board
        """
        session_state.set_form_values({"automation_status": []})
        raw = {
            "cases": [
                {
                    "id": 1,
                    "title": "Case A",
                    "priority_id": 3,
                    "custom_automation_status": 2,
                },
                {
                    "id": 2,
                    "title": "Case B",
                    "priority_id": 1,
                    "custom_automation_status": 1,
                },
            ]
        }

        board = controller.normalize_and_save_data(raw)
        # Ensure board columns include expected titles
        titles = {col["title"] for col in board}
        for status in controller.status_translation.values():
            assert status in titles

        # Ensure cards placed in correct columns
        status_priority = [(1, 1), (3, 2)]
        for priority_id, status_code in status_priority:
            status = controller.status_translation[status_code]
            column = next(filter(lambda val: val["title"] == status, board), None)
            assert column is not None, f"Column '{status}' not found"
            assert column["cards"], f"No test cases were saved in {column['cards']}"
            test_case = column["cards"][0]
            # Ensure fields contain translated priority name
            assert test_case["fields"] == [
                f"{controller.priority_translation[priority_id]}"
            ]
            # Ensure colors applied
            assert test_case["color"] == Util.priority_color(priority_id)
        # Saved to state
        assert session_state.get_initial_board() == board

    def test_normalize_and_save_data_handles_empty_cases(
        self, session_state, controller
    ):
        session_state.set_form_values({"automation_status": []})
        board = controller.normalize_and_save_data({"cases": []})
        assert isinstance(board, list)
        assert all("cards" in col for col in board)
        assert session_state.get_initial_board() == board
