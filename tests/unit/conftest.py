import pytest
import json
from pytest_httpserver import HTTPServer

from random import randint

CREATE_RESPONSE_FILE = "tests/unit/create_response.json"

def set_response(payload: dict) -> dict:
    changes = {}
    for k, v in payload.items():
        if v == "%Ibug_id":
            changes[k] = randint(1000,5000)
    for change in changes:
        payload[change] = changes[change]

    return payload


@pytest.fixture()
def mock_bugzilla(httpserver: HTTPServer):
    httpserver.expect_request(
        "/rest/bug",
        query_string={
            "api_key": "abcdefghijklmnop"
        },
        json={
            "component": "STArFox",
            "product": "Mozilla QA",
            "summary": "Test Bug Please Ignore",
            "version": "unspecified",
            "type": "task"
        },
        method="POST"
    ).respond_with_json(
        set_response(json.load(open(CREATE_RESPONSE_FILE)))
    )
    yield httpserver
