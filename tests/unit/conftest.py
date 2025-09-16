import pytest
import json
from pytest_httpserver import HTTPServer
from datetime import datetime

from random import randint

CREATE_RESPONSE_FILE = "tests/unit/create_response.json"
UPDATE_RESPONSE_FILE = "tests/unit/update_response.json"


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
        json={
            "component": "STArFox",
            "product": "Mozilla QA",
            "summary": "Test Bug Please Ignore",
            "version": "unspecified",
            "type": "task",
        },
        method="POST",
    ).respond_with_json(set_response(json.load(open(CREATE_RESPONSE_FILE))))
    httpserver.expect_request(
        "/rest/bug",
        query_string={"api_key": "abcdefghijklmnop"},
        json={"ids": [1234], "blocks": {"add": [4321]}},
        method="PUT",
    ).respond_with_json(set_response(json.load(open(UPDATE_RESPONSE_FILE))))
    httpserver.expect_request("/rest/bug")
    yield httpserver
