import pytest
import json
from pytest_httpserver import HTTPServer
from pathlib import Path
from unittest.mock import MagicMock

from src.core.state import SessionState
from src.core.triage import Triage

SOURCE_LOC = "tests/unit"

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
def state():
    return SessionState({"state": True})

@pytest.fixture
def triage(state, mock_tr_session):
    return Triage(state=state)

def get_payload(endpoint, payload_type):
    return json.load(Path(SOURCE_LOC, f"{endpoint}_{payload_type}.json").open())


@pytest.fixture()
def mock_bugzilla(httpserver: HTTPServer):
    httpserver.expect_request(
        "/rest/bug",
        query_string={"api_key": "abcdefghijklmnop"},
        json=get_payload("create", "request"),
        method="POST",
    ).respond_with_json(get_payload("create", "response"))
    httpserver.expect_request(
        "/rest/bug",
        query_string={"api_key": "abcdefghijklmnop"},
        json=get_payload("update", "request"),
        method="PUT",
    ).respond_with_json(get_payload("update", "response"))
    httpserver.expect_request("/rest/bug")
    yield httpserver
