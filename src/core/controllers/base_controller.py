from src.core.state import SessionState


class BaseController:
    def __init__(self, state=None):
        self.state = state if state else SessionState()
        self.status_translation = {
            1: "Status Untriaged",
            2: "Status Suitable",
            3: "Status Unsuitable",
            4: "Status Completed",
            5: "Status Disabled"
        }
        self.priority_translation = {
            1: "Priority Low",
            2: "Priority Medium",
            3: "Priority High",
            4: "Priority Critical"
        }
        self.csv_headers = ["Test Case ID", "Original Status", "Current Status"]
