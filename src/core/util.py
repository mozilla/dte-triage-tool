from src.config.types import KanbanColumn


class Util:
    def __init__(self):
        self.status_translation = {
            1: "Status Untriaged",
            2: "Status Suitable",
            3: "Status Unsuitable",
            4: "Status Completed",
            5: "Status Disabled",
        }
        self.inverted_status_translation = {
            v.lower(): k for k, v in self.status_translation.items()
        }

    @staticmethod
    def priority_color(priority_id):
        """
        Return a hex color based on priority_id.
        Adjust mappings as needed to match your TestRail priorities.
        """
        mapping = {
            4: "#e53935",  # Critical - Red
            3: "#fb8c00",  # High - Orange
            2: "#fdd835",  # Medium - Yellow
            1: "#43a047",  # Low - Green
        }
        return mapping.get(int(priority_id), "#9e9e9e")  # Default - Grey

    @staticmethod
    def extract_and_concat_ids(data: list[tuple[int, str]]) -> str:
        """
        Give a tuple entry of an int and str, extract the int ids and return a comma-separated string of the ids.
        """
        return ",".join([str(id) for id, _ in data])

    @staticmethod
    def extract_section_name_and_ids(sections: list[dict]) -> list[tuple[int, str]]:
        """Given the section information for a given project and suite, extract the section name and ids."""
        return [(section.get("id"), section.get("name")) for section in sections]

    @staticmethod
    def extract_case_ids_from_board(status_code: int, board: list[KanbanColumn]):
        """
        Given a status code and a board list, extract the case ids for the given status code.
        """
        return [card["id"] for card in board[status_code - 1]["cards"]]

    @staticmethod
    def index_cases_by_status(board: list[KanbanColumn]):
        """
        Given a board list, map the test cases by automation status.
        """
        cases_by_status = {}
        for col in board:
            cases_by_status[col["id"]] = col["cards"]
        return cases_by_status

    def update_initial_board(self, board: list[KanbanColumn], status_map: dict[str, list[str]]):
        """Update the initial board with the test cases grouped by automation status."""
        for case_id, status_change in status_map.items():
            prev_idx = self.inverted_status_translation.get(status_change[0]) - 1
            cur_idx = self.inverted_status_translation.get(status_change[1]) - 1
            for idx, case in enumerate(board[prev_idx]["cards"]):
                if case.get("id") == case_id:
                    board[cur_idx]["cards"].append(case)
                    board[prev_idx]["cards"].pop(idx)
                    break
        return board