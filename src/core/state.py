import time
from collections import defaultdict
from typing import Optional, Any

import streamlit as st
from streamlit_local_storage import LocalStorage
from src.config.types import FormValues, SessionKey, Priority, KanbanColumn
from src.core.util import Util


class SessionState:
    """
    Thin wrapper for typed session state access.
    """

    def __init__(self, state=None):
        self._state = state if state is not None else st.session_state
        self.local_storage = LocalStorage()
        self.util = Util()

    # Local Storage Helpers

    def _persist(self, item_key, value: any):
        """Helper to save to local storage"""
        self.local_storage.setItem(item_key, value, key=item_key.value)

    def _load_from_storage(self, key: str):
        """Helper to load from local storage if session state is missing it"""
        if key not in self._state:
            stored_value = self.local_storage.getItem(key)
            if stored_value:
                if key == SessionKey.STATUS_MAP and self.has_initial_board():
                    self.util.update_initial_board(
                        self.get_initial_board(), stored_value
                    )
                self._state[key] = stored_value

    def sync_all_from_storage(self):
        """Call this once on app startup to re-hydrate session state"""
        for key in SessionKey:
            self._load_from_storage(key)

    def sync_all_to_storage(self):
        """Call this once on app exit to persist session state"""
        self.local_storage.deleteAll()
        for key in SessionKey:
            self._persist(key, self._state.get(key))

    # Generic helpers

    def _get(self, key: SessionKey, default=None) -> Any:
        return self._state.get(key, default)

    def _set(self, key: SessionKey, value: Any):
        if key in self._state:
            self._clear(key)
        self._state[key] = value

    def _clear(self, key: SessionKey):
        self._state.pop(key, None)

    def _clear_local_storage(self, key: SessionKey):
        self.local_storage.eraseItem(key, key=key.value)

    def _has(self, key: SessionKey) -> bool:
        return key in self._state and self._state[key] not in (None, {}, [], "")

    def clear_state_values(self, excluded_states):
        """Clear all session state values except priorities"""
        if self.local_storage.getAll():
            self.local_storage.deleteAll(key="clear_state_values")
        for key in SessionKey:
            if key not in excluded_states:
                self._clear(key)

    # Form Values

    def get_form_values(self) -> Optional[FormValues]:
        return self._get(SessionKey.FORM_VALUES, {})

    def set_form_values(self, values: FormValues):
        if self._has(SessionKey.FORM_VALUES):
            self.get_form_values().update(values)
        else:
            self._set(SessionKey.FORM_VALUES, values)

    def has_form_values(self) -> bool:
        fv = self.get_form_values()
        required = ("suite_id", "priority_id", "automation_status")
        return all(fv.get(k) for k in required)

    def clear_form_values(self):
        self._clear(SessionKey.FORM_VALUES)

    # Priorities

    def get_priorities(self) -> Optional[list[Priority]]:
        return self._get(SessionKey.AVAILABLE_PRIORITIES)

    def set_priorities(self, priorities: list[Priority]):
        self._set(SessionKey.AVAILABLE_PRIORITIES, priorities)

    def has_priorities(self) -> bool:
        return self._has(SessionKey.AVAILABLE_PRIORITIES)

    def clear_priorities(self):
        self._clear(SessionKey.AVAILABLE_PRIORITIES)

    # Initial Kanban Board

    def get_initial_board(self) -> Optional[list[KanbanColumn]]:
        return self._get(SessionKey.INITIAL_BOARD)

    def set_initial_board(self, board: list[KanbanColumn]):
        self.clear_initial_board()
        self._set(SessionKey.INITIAL_BOARD, board)

    def has_initial_board(self) -> bool:
        return self._has(SessionKey.INITIAL_BOARD)

    def clear_initial_board(self):
        self._clear(SessionKey.INITIAL_BOARD)

    # Status Map

    def get_status_map(self):
        return self._get(SessionKey.STATUS_MAP)

    def set_status_map(self, status_map):
        self._set(SessionKey.STATUS_MAP, status_map)

    def has_status_map(self):
        return self._has(SessionKey.STATUS_MAP)

    def clear_status_map(self):
        self._clear(SessionKey.STATUS_MAP)

    # Search Params

    def get_search_params(self):
        return self._get(SessionKey.SEARCH_PARAMS)

    def set_search_params(self, key: str, params):
        if not self.has_search_params():
            self._set(SessionKey.SEARCH_PARAMS, defaultdict(list))
        self._state[SessionKey.SEARCH_PARAMS][key] = params

    def has_search_params(self):
        return self._has(SessionKey.SEARCH_PARAMS)

    def clear_search_params(self):
        self._clear(SessionKey.SEARCH_PARAMS)
