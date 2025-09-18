import json
import os

import pytest

current_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(current_dir, "data")


@pytest.fixture
def load_data():
    def _load(name: str):
        with open(os.path.join(DATA_DIR, name)) as f:
            return json.load(f)

    return _load


class TestTriage:
    def test_fetch_test_cases_parametrized(self, triage, mock_tr_session, load_data):
        # get data and save in variables
        data = load_data('fetch_test_cases.json')
        input_data = data['input']
        mock_output = data['output']
        expected_data = data['expected']
        mock_tr_session.get_test_cases.return_value = mock_output
        out = triage.fetch_test_cases(input_data)
        assert out == expected_data
        mock_tr_session.get_test_cases.assert_called_once_with(input_data)

    def test_get_and_cache_priorities_empty_state(self, triage, session_state, mock_tr_session, load_data):
        mock_output = load_data('get_and_cache_priorities.json')['output']
        mock_tr_session.get_priorities.return_value = mock_output
        out = triage.get_and_cache_priorities()
        assert out == mock_output
        mock_tr_session.get_priorities.assert_called_once()
        assert session_state.get_priorities() == mock_output

    def test_get_and_cache_priorities_populated_state(self, triage, session_state, mock_tr_session, load_data):
        mock_output = load_data('get_and_cache_priorities.json')['output']
        session_state.set_priorities(mock_output)
        triage.get_and_cache_priorities()
        mock_tr_session.get_priorities.assert_not_called()