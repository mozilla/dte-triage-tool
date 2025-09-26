from unittest import mock
from src.core.integrations.testrail_integration import TestRail


def test_bugzilla_payload_gen(load_data):
    mock_testrail = TestRail(
        "https://testrail.example.com",
        "fakeuser",
        "fakepass"
    )
    data = load_data("bugzilla_payload")
    get_suite_return = data.get("output").get("get_suite")
    get_case_return = data.get("output").get("get_case")
    with mock.patch.object(mock_testrail, "get_suite", return_value=get_suite_return):
        with mock.patch.object(mock_testrail, "get_case", return_value=get_case_return):
            test_input = data.get("input")
            out = mock_testrail.get_bugzilla_content(**test_input)
            assert out == data.get("expected")
