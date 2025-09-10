from typing import Optional

from src.config.types import FormValues, SessionKey, Priority, KanbanColumn
import streamlit as st


class SessionState:
    """
    Thin wrapper to control session state.
    """

    def __init__(self, state=None):
        """Initialize the state but can also pass in a pre-existing state for testing"""
        self._state = state if state else st.session_state

    # Form values
    def get_form_values(self) -> Optional[FormValues]:
        return self._state.get(SessionKey.FORM_VALUES)

    def set_form_values(self, values: FormValues):
        self._state[SessionKey.FORM_VALUES] = values

    def has_form_values(self):
        fv = self.get_form_values()
        if not fv:
            return False
        required = ("suite_id", "priority_id", "automation_status")
        return all(k in fv and fv.get(k) for k in required)

    def clear_form_values(self):
        if self.has_form_values():
            del self._state[SessionKey.FORM_VALUES]

    # Priorities
    def get_priorities(self) -> list[Priority] | None:
        return self._state.get(SessionKey.AVAILABLE_PRIORITIES)

    def set_priorities(self, priorities: list[Priority]):
        self._state[SessionKey.AVAILABLE_PRIORITIES] = priorities

    def has_priorities(self):
        return self.get_priorities() is not None

    def clear_priorities(self):
        if self.has_priorities():
            del self._state[SessionKey.AVAILABLE_PRIORITIES]

    # Initial Board data (Test cases)
    def get_initial_board(self) -> list[KanbanColumn] | None:
        return self._state.get(SessionKey.INITIAL_BOARD)

    def set_initial_board(self, test_cases: list[KanbanColumn]):
        self._state[SessionKey.INITIAL_BOARD] = test_cases

    def has_initial_board(self):
        return self.get_initial_board() is not None

    def clear_initial_board(self):
        if self.has_initial_board():
            del self._state[SessionKey.INITIAL_BOARD]

    # Current Board
    def get_board(self) -> list[KanbanColumn] | None:
        return self._state.get(SessionKey.CURRENT_BOARD)

    def set_board(self, board: list[KanbanColumn]):
        self._state[SessionKey.CURRENT_BOARD] = board

    def has_board(self):
        return self.get_board() is not None

    def clear_board(self):
        if self.has_board():
            del self._state[SessionKey.CURRENT_BOARD]
