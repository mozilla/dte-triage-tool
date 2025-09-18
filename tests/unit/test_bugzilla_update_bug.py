from src.core.integrations.bugzilla_integration import Bugzilla


def test_create_bug(mock_bugzilla):
    bz = Bugzilla(mock_bugzilla.url_for(""), local=True)
    bz.client.api_key = "abcdefghijklmnop"
    bz.update_bug(bug_ids=[1234], payload={"blocks": {"add": [4321]}})
