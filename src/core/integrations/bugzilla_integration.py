from os import environ
from src.core.integrations.api import BugzillaAPIClient


class Bugzilla:
    def __init__(self, host, local=False):
        self.client = BugzillaAPIClient(host, local)
        if not local and not environ.get("BUGZILLA_API_KEY"):
            raise BugzillaAPIClient.APIError("Bugzilla instance requires an API key")
        else:
            self.client.api_key = environ.get("BUGZILLA_API_KEY")

    def get_bug(self, bug_id, secure=False):
        return self.client.send_get("rest/bug", params={"id": bug_id}, secure=secure)

    def create_bug(self, summary: str, product="Mozilla QA", component="STArFox"):
        return self.client.send_post(
            "rest/bug",
            data={
                "component": component,
                "product": product,
                "summary": summary,
                "version": "unspecified",
                "type": "task",
            },
            secure=True,
        )

    def update_bug(self, bug_ids: list, payload: dict):
        return self.client.send_put(
            "rest/bug", data={"ids": bug_ids, **payload}, secure=True
        )
