import pytest
from src.core.util import Util


class TestUtil:
    @pytest.mark.parametrize(
        "priority_id, expected",
        [
            (4, "#e53935"),
            (3, "#fb8c00"),
            (2, "#fdd835"),
            (1, "#43a047"),
            (0, "#9e9e9e"),
            (999, "#9e9e9e"),
        ],
    )
    def test_priority_color(self, priority_id, expected):
        assert Util.priority_color(priority_id) == expected

    @pytest.mark.parametrize(
        "data, expected",
        [
            ([], ""),
            ([(1, "Low")], "1"),
            ([(1, "Low"), (3, "High"), (2, "Medium")], "1,3,2"),
        ],
    )
    def test_extract_and_concat_ids(self, data, expected):
        assert Util.extract_and_concat_ids(data) == expected

    def test_index_cases_by_status(self):
        board = [
            {"id": "status-untriaged", "cards": [{"id": "1"}, {"id": "2"}]},
            {"id": "status-suitable", "cards": [{"id": "3"}]},
        ]
        result = Util.index_cases_by_status(board)
        assert result["status-untriaged"] == [{"id": "1"}, {"id": "2"}]
        assert result["status-suitable"] == [{"id": "3"}]
        assert len(result.keys()) == 2
