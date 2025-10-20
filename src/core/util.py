from src.config.types import KanbanColumn
from src.core.state import SessionState


class Util:
    def __init__(self):
        self.session_state = SessionState()

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
    def extract_case_ids_from_board(status_code: int, board: list[KanbanColumn]):
        """
            Given a status code and a board list, extract the case ids for the given status code.
        """
        return [card['id'] for card in board[status_code - 1]['cards']]

    @staticmethod
    def index_cases_by_status(board: list[KanbanColumn]):
        """
            Given a board list, map the test cases by automation status.
        """
        cases_by_status = {}
        for col in board:
            cases_by_status[col["id"]] = col["cards"]
        return cases_by_status
