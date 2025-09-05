from src.config.types import KanbanColumn
from src.core.state import SessionState
from src.core.util import Util


class BoardController:
    """
        class to control changes in the board.
    """

    def __init__(self, state=None):
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

    def update_board(self, board):
        self.state.clear_board()
        self.state.set_board(board)

    def normalize_and_save_data(self, test_cases: dict[str, list[dict] | dict]) -> list[KanbanColumn]:
        """
            Takes the test case data and formats it for the kanban board view and saves it to the session state.
        """
        test_cases = test_cases.get('cases', [])
        cols: dict[str, KanbanColumn] = {
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
        initial_board = list(cols.values())
        self.state.set_initial_board(initial_board)
        self.state.set_board(initial_board)
        return initial_board

    # def map_status_transitions(self):
    #     """
    #         Map the status transitions between the initial and current board states.
    #     """
    #     initial_board_state = Util.index_cases_by_status(self.state.get_initial_board())
    #     current_board_state = Util.index_cases_by_status(self.state.get_board())
    #     status_transitions = {}
    #     for status in self.status_translation.values():
    #         initial_cases = initial_board_state[status.lower()]
    #         current_cases = current_board_state[status.lower()]
    #         if current_cases > initial_cases:
