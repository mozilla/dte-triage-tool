import pytest
import json
from pytest_httpserver import HTTPServer
from pathlib import Path


SOURCE_LOC = "tests/unit"


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
