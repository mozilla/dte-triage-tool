from enum import Enum
from typing import TypedDict, Tuple


class FormValues(TypedDict):
    """Input values for the form."""

    project_id: int
    project_name: str
    limit: int
    suite_id: int
    suite_name: str
    priority_id: list[Tuple[int, str]]
    automation_status: list[Tuple[int, str]]


class SessionKey(str, Enum):
    """Session state keys."""

    FORM_VALUES = "form_values"
    INITIAL_BOARD = "initial_board"
    AVAILABLE_PRIORITIES = "available_priorities"
    STATUS_MAP = "test_case_status_map"


class Priority(TypedDict):
    """Priority object."""

    id: int
    priority: int
    name: str
    short_name: str
    is_default: bool


class TestCase(TypedDict):
    """TestCase object."""

    id: int
    name: str
    fields: list[str]
    color: str


class KanbanColumn(TypedDict):
    """KanbanColumn object."""

    id: str
    title: str
    cards: list[TestCase]
