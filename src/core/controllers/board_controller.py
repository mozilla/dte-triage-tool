from src.config.types import KanbanColumn
from src.core.controllers.base_controller import BaseController
from src.core.util import Util
import pandas as pd


class BoardController(BaseController):
    """
    class to control changes in the board.
    """

    def __init__(self, state=None):
        super().__init__(state)

    def update_status_map(self, updated_cases):
        """Update the status map for test cases."""
        self.state.clear_status_map()
        self.state.set_status_map(updated_cases)

    def format_status_map(self):
        """format the updated status map for the kanban board to csv format."""
        current_status_map = self.state.get_status_map()
        status_map = [
            {"Test Case ID": k, "Original Status": v[0], "Current Status": v[1]}
            for k, v in current_status_map.items()
        ]
        df = pd.DataFrame(status_map, columns=self.csv_headers)
        return df

    def normalize_and_save_data(
        self, test_cases: dict[str, list[dict] | dict]
    ) -> list[KanbanColumn]:
        """
        Takes the test case data and formats it for the kanban board view and saves it to the session state.
        """
        test_cases = test_cases.get("cases", [])
        cols: dict[str, KanbanColumn] = {
            status: {"id": status.lower(), "title": status, "cards": []}
            for status in self.status_translation.values()
        }
        for test_case in test_cases:
            case_automation_status = self.status_translation[
                test_case["custom_automation_status"]
            ]
            cols[case_automation_status]["cards"].append(
                {
                    "id": str(test_case["id"]),
                    "name": test_case["title"],
                    "fields": [
                        f"{self.priority_translation[test_case['priority_id']]}"
                    ],
                    "color": Util.priority_color(test_case["priority_id"]),
                }
            )
        initial_board = list(cols.values())
        self.state.set_initial_board(initial_board)
        return initial_board
