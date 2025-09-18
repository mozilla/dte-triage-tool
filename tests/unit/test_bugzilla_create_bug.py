from src.core.integrations.bugzilla_integration import Bugzilla


def test_create_bug(mock_bugzilla):
    bz = Bugzilla(mock_bugzilla.url_for(""), local=True)
    bz.client.api_key = "abcdefghijklmnop"
    bz.create_bug(summary="Test Bug Please Ignore")
