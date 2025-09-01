from src.core.state import SessionState
from src.core.triage import Triage
from src.core.types import FormValues


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
            1: "#e53935",  # Critical - Red
            2: "#fb8c00",  # High - Orange
            3: "#fdd835",  # Medium - Yellow
            4: "#43a047",  # Low - Green
            5: "#1e88e5",  # Very Low - Blue
        }
        return mapping.get(int(priority_id), "#9e9e9e")  # Default - Grey

    @staticmethod
    def extract_and_concat_ids(data: list[tuple[int, str]]) -> str:
        """
            Give a tuple entry of an int and str, extract the int ids and return a comma separated string of the ids.
        """
        return ",".join([str(id) for id, _ in data])
