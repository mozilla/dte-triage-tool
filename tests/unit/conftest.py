import pytest
import json
from pytest_httpserver import HTTPServer
from datetime import datetime
from pathlib import Path

from random import randint

SOURCE_LOC = "tests/unit"
def get_payload(endpoint, payload_type):
    return json.load(Path(SOURCE_LOC, f"{endpoint}_{payload_type}.json").open())

def create_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def set_response(payload: dict) -> dict:
    changes = {}
    for k, v in payload.items():
        if v == "%Ibug_id":
            changes[k] = randint(1000, 5000)
        elif v == "%bug_id":
            changes[k] = str(randint(1000, 5000))
        elif v == "%timestamp":
            changes[k] = create_timestamp()
    for change in changes:
        payload[change] = changes[change]

    return payload


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
