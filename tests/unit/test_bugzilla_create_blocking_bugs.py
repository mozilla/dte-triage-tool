import json
from src.core.integrations.bugzilla_integration import Bugzilla
from unittest import mock
from contextlib import ExitStack
from copy import deepcopy
import logging

import pytest


@pytest.mark.parametrize("db_case", [1, 2, 3])
def test_create_blocking_bugs(load_data, db_case):
    mock_bz_db = load_data(f"bugzilla_database_{db_case}")

    def search_bug(query):
        bugs = deepcopy(mock_bz_db)
        for field, term in query.items():
            logging.warning(f"search {field}: {term}")
            logging.warning("\n".join([bug.get(field) for bug in bugs]))
            bugs = [bug for bug in bugs if bug.get(field) == term]
        return {"bugs": bugs}

    def get_bug(bug_id):
        return {"bugs": [bug for bug in mock_bz_db if bug.get("id") == bug_id]}

    def create_bug(**kwargs):
        mock_bz_db.append({"id": len(mock_bz_db) + 1, **kwargs})
        return {"id": len(mock_bz_db)}

    def update_bug(bug_ids: list, payload: dict):
        logging.warning(f"UPDATE:\nBUGS: {bug_ids}\n===\n{payload}")
        changes = {"bugs": []}
        for bug_id in bug_ids:
            logging.warning(f"updating bug {bug_id}")
            logging.warning(f"blocks: {payload.get('blocks')}")
            for cmd, block_ids in payload.get("blocks").items():
                if cmd == "add":
                    idx = mock_bz_db.index(get_bug(bug_id)["bugs"][0])
                    mock_bz_db[idx] |= {"blocks": block_ids}
                    for add in block_ids:
                        idx = mock_bz_db.index(get_bug(add)["bugs"][0])
                        if not mock_bz_db[idx].get("depends_on"):
                            mock_bz_db[idx]["depends_on"] = [bug_id]
                        else:
                            mock_bz_db[idx]["depends_on"].append(bug_id)
            changes["bugs"].append(
                {
                    "id": bug_id,
                    "changes": {
                        "blocks": {"removed": "", "added": payload.get("blocks")}
                    },
                }
            )
        return changes

    mock_bugzilla = Bugzilla("https://bugzilla.example.com")
    data = load_data("bugzilla_structure")
    mock_methods = ["get_bug", "search_bug", "create_bug", "update_bug"]
    test_input = data.get("input")
    contexts = [
        mock.patch.object(mock_bugzilla, method, wraps=locals().get(method))
        for method in mock_methods
    ]
    with ExitStack() as exit_stack:
        for cm in contexts:
            exit_stack.enter_context(cm)
        mock_bugzilla.create_bug_structure(**test_input)
        # assert data.get("expected") == out
        with open("test_output.json", "w") as fh:
            json.dump(mock_bz_db, fh, indent=2)
        assert mock_bz_db == load_data("bugzilla_database_key")
