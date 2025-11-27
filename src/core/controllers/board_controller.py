from src.config.types import KanbanColumn, FormValues
from src.core.controllers.base_controller import BaseController
from src.core.util import Util
import pandas as pd


class BoardController(BaseController):
    """
    class to control changes in the board.
    """

    def __init__(self, state=None):
        super().__init__(state)

    def update_status_map(self, updated_status_map):
        """Update the status map for test cases."""
        existing_status_map = self.state.get_status_map() or {}
        # Merge, updated cases override
        merged = existing_status_map | updated_status_map

        # Filter out cases where the change cancels itself out
        # only add to the final status map if:
        #   case id isn't present in the existing status map OR updated status up
        #   and if there present in both, make sure the initial state of the existing status map isn't the same as the updated status final state.
        cleaned = {
            cid: status for cid, status in merged.items() if
            (not existing_status_map.get(cid)) or (not updated_status_map.get(cid)) or (
                        updated_status_map.get(cid)[0] != existing_status_map.get(cid)[1])
        }
        self.state.set_status_map(cleaned)

    def format_status_map(self):
        """format the updated status map for the kanban board to csv format."""
        current_status_map = self.state.get_status_map()
        form_value: FormValues = self.state.get_form_values()
        status_map = []
        for k, v in current_status_map.items():
            item = {
                "Project ID": form_value.get("project_id"),
                "Suite ID": form_value.get("suite_id"),
                "Test Case ID": k,
                "Original Status": v[0],
                "Current Status": v[1],
            }
            status_map.append(item)
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
        rotations = set()
        rotation_filter = self.state.get_form_values().get("custom_rotation")
        automation_status_filter = [
            status[0]
            for status in self.state.get_form_values().get("automation_status")
        ]
        for test_case in test_cases:
            if rotation_filter and test_case.get("custom_rotation") != rotation_filter:
                continue
            if (
                    automation_status_filter
                    and test_case.get("custom_automation_status")
                    not in automation_status_filter
            ):
                continue
            if test_case.get("custom_rotation"):
                rotations.add(test_case.get("custom_rotation"))
            case_automation_status = self.status_translation.get(
                test_case.get("custom_automation_status"), "Status Untriaged"
            )
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
        if not (
                self.state.has_search_params()
                and "rotations" in self.state.get_search_params()
        ):
            self.state.set_search_params("rotations", list(rotations))
        self.state.set_initial_board(initial_board)
        return initial_board
