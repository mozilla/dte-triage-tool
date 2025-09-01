from enum import Enum
from typing import TypedDict, Literal, Tuple


class FormValues(TypedDict):
    """ Input values for the form. """
    suite_id: int
    priority_id: list[Tuple[int, str]]
    automation_status: list[Tuple[int, str]]

class SessionKey(str, Enum):
    """ Session state keys. """
    FORM_VALUES = "form_values"
    TEST_CASES = "test_cases"
    AVAILABLE_PRIORITIES = "available_priorities"

class Priority(TypedDict):
    """ Priority object. """
    id: int
    priority: int
    name: str
    short_name: str
    is_default: bool
