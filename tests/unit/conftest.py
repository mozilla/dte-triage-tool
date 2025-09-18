import pytest
from unittest.mock import MagicMock

from src.core.state import SessionState
from src.core.triage import Triage


@pytest.fixture(autouse=True)
def reset_singleton():
    Triage._instance = None
    yield
    Triage._instance = None


@pytest.fixture
def mock_tr_session(mocker):
    mock_tr = mocker.patch("src.core.triage.TestRail")
    mock = MagicMock()
    mock_tr.return_value = mock
    return mock

@pytest.fixture
def session_state():
    return SessionState({"state": True})

@pytest.fixture
def triage(session_state, mock_tr_session):
    return Triage(state=session_state)
