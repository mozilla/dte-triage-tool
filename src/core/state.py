from typing import Any, Optional

from src.config.types import FormValues, SessionKey, Priority
import streamlit as st


class SessionState:
    """
    Thin wrapper to control session state.
    """

    def __init__(self, state=None):
        """Initialize the state but can also pass in a pre-existing state for testing"""
        self._state = state if state else st.session_state

    # Form values
    def set_form_values(self, values: FormValues):
        self._state[SessionKey.FORM_VALUES] = values

    def get_form_values(self) -> Optional[FormValues]:
        return self._state.get(SessionKey.FORM_VALUES)

    def has_form_values(self):
        fv = self.get_form_values()
        if not fv:
            return False
        required = ("suite_id", "priority_id", "automation_status")
        return all(k in fv and fv.get(k) for k in required)

    def clear_form_values(self):
        if self.has_form_values():
            del self._state[SessionKey.FORM_VALUES]

    # Test cases
    def set_test_cases(self, test_cases: list[Any]):
        self._state[SessionKey.TEST_CASES] = test_cases

    def get_test_cases(self):
        return self._state.get(SessionKey.TEST_CASES)

    def has_test_cases(self):
        return self.get_test_cases() is not None

    def clear_test_cases(self):
        if self.has_test_cases():
            del self._state[SessionKey.TEST_CASES]

    # Priorities
    def set_priorities(self, priorities: list[Priority]):
        self._state[SessionKey.AVAILABLE_PRIORITIES] = priorities

    def get_priorities(self) -> list[Priority] | None:
        return self._state.get(SessionKey.AVAILABLE_PRIORITIES)

    def has_priorities(self):
        return self.get_priorities() is not None

    def clear_priorities(self):
        if self.has_priorities():
            del self._state[SessionKey.AVAILABLE_PRIORITIES]
