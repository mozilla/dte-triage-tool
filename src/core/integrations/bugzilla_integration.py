from os import environ
from typing import Tuple
from src.core.integrations.api import BugzillaAPIClient
from pathlib import Path

TEMPLATE_LOC = "src/data"
DEFAULT_CREATE_PAYLOAD = {
    "component": "STArFox",
    "product": "Mozilla QA",
    "summary": "Test Bug Please Ignore",
    "version": "unspecified",
    "type": "task"
}

def populate_template(structure, element, content, case_id=None):
    loc = Path(TEMPLATE_LOC, f"bugzilla_{structure}_template_{element}.md")
    with loc.open() as fh:
        output = fh.read()
    for field in content:
        if field == "cases":
            if not case_id:
                continue
            for subfield in content[field]:
                output = output.replace(f"%{subfield}%", content[field][subfield])
        else:
            output = output.replace(f"%{field}%", content[field])
    return output

class Bugzilla:
    def __init__(self, host, local=False):
        self.client = BugzillaAPIClient(host, local)
        if not local and not environ.get("BUGZILLA_API_KEY"):
            raise BugzillaAPIClient.APIError("Bugzilla instance requires an API key")
        else:
            self.client.api_key = environ.get("BUGZILLA_API_KEY")

    def get_bug(self, bug_id, secure=False):
        return self.client.send_get("rest/bug", params={"id": bug_id}, secure=secure)

    def search_bug(self, query_tuple: Tuple, secure=False):
        return self.client.send_get("rest/bug", params=query_tuple)

    def create_bug(self, summary: str, product="Mozilla QA", component="STArFox", **kwargs):
        return self.client.send_post(
            "rest/bug",
            data={
                "component": component,
                "product": product,
                "summary": summary,
                "version": "unspecified",
                "type": "task",
                **kwargs
            },
            secure=True,
        )

    def update_bug(self, bug_ids: list, payload: dict):
        return self.client.send_put(
            "rest/bug", data={"ids": bug_ids, **payload}, secure=True
        )

    def create_blocking_bugs(self, parameter_sets, blocked_bug_id):
        new_bug_ids = []
        for parameters in parameter_sets:
            payload = DEFAULT_CREATE_PAYLOAD | parameters
            new_bug_ids.append(self.create_bug(**payload).get("id"))
        update_response = self.update_bug(
            new_bug_ids,
            {
                "blocks": {
                    "add": [blocked_bug_id]
                }
            }
        )
        return [bug.get("id") for bug in update_response.get("bugs")]

    def create_blocking_bug(self, parameters, blocked_bug_id):
        return self.create_blocking_bugs(
    [parameters], blocked_bug_id
        )[0]

    def create_bug_structure(self, root_bug_id, content_payload):
        suite_bug_name = populate_template("suite", "title", content_payload)
        search_response = self.search_bug(("summary", suite_bug_name))
        matching_bugs = search_response.get("bugs")
        if not matching_bugs:
            suite_bug_body = populate_template("suite", "body", content_payload)
            suite_bug = self.create_blocking_bug(
                {
                    "summary": suite_bug_name,
                    "description": suite_bug_body,
                },
                root_bug_id
            )
        elif len(matching_bugs) == 1:
            suite_bug = matching_bugs[0]
        else:
            # TODO: is this case an error?
            suite_bug = matching_bugs[0]
        case_params = []
        for case_ in content_payload.get("cases"):
            case_bug_name = populate_template("case", "title", case_)
            case_matches = self.search_bug(("summary", case_bug_name))
            if not case_matches.get("bugs"):
                case_bug_body = populate_template("case", "body", case_)
                case_params.append(
                    {
                        "summary": case_bug_name,
                        "description": case_bug_body,
                    }
                )
            if case_params:
                self.create_blocking_bugs(case_params, suite_bug)

