from os import environ
from src.core.integrations.api import BugzillaAPIClient
from pathlib import Path
import logging
import re

TEMPLATE_LOC = "src/data"
DEFAULT_CREATE_PAYLOAD = {
    "component": "STArFox",
    "product": "Mozilla QA",
    "summary": "Test Bug Please Ignore",
    "version": "unspecified",
    "type": "task",
}
DEFAULT_BLOCK_SEARCH_PAYLOAD = {
    "query_format": "advanced",
    "o1": "anyexact",
    "j_top": "OR",
    "f1": "blocked",
    "v1": 1976270,
}
FUNCTIONAL_ROOT_METABUG = 1976270


def populate_template(structure, element, content, case_id=None):
    loc = Path(TEMPLATE_LOC, f"bugzilla_{structure}_template_{element}.md")
    with loc.open() as fh:
        output = fh.read().strip()
    for field in content:
        if field == "cases":
            if not case_id:
                continue
            for subfield in content[field]:
                output = output.replace(f"%{subfield}%", str(content[field][subfield]))
        output = output.replace(f"%{field}%", str(content[field]))
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

    def search_bug(self, query_payload: dict, secure=False):
        return self.client.send_get("rest/bug", params=query_payload, secure=secure)

    def search_bug_by_block(self, block: int, secure=False):
        return self.client.send_get(
            "rest/bug",
            params=DEFAULT_BLOCK_SEARCH_PAYLOAD | {"v1": block},
            secure=secure,
        )

    def create_bug(
        self, summary: str, product="Mozilla QA", component="STArFox", **kwargs
    ):
        return self.client.send_post(
            "rest/bug",
            data={
                "component": component,
                "product": product,
                "summary": summary,
                "version": "unspecified",
                "type": "task",
                **kwargs,
            },
            secure=True,
        )

    def update_bug(self, bug_ids: list, payload: dict):
        return self.client.send_put(
            f"rest/bug/{bug_ids[0]}", data={"ids": bug_ids, **payload}, secure=True
        )

    def create_blocking_bugs(self, parameter_sets, blocked_bug_id):
        new_bug_ids = []
        for parameters in parameter_sets:
            logging.warning(f"parameter set: {parameters}")
            payload = DEFAULT_CREATE_PAYLOAD | parameters
            new_bug_id = self.create_bug(**payload).get("id")
            logging.warning(f"Created bug {new_bug_id}")
            new_bug_ids.append(new_bug_id)
        update_response = self.update_bug(
            new_bug_ids, {"blocks": {"add": [blocked_bug_id]}}
        )
        return [bug.get("id") for bug in update_response.get("bugs")]
    def create_blocking_bug(self, parameters, blocked_bug_id):
        return self.create_blocking_bugs([parameters], blocked_bug_id)[0]

    def find_bugs_by_test_case_id(self, case_id: str, parent_bug_id: int = FUNCTIONAL_ROOT_METABUG):
        """
            Given a suite bug id and a test case id, find all the test case bugs that are blocked on the suite bug.
            If no suite bug is provided, use the functional root metabug.
        """
        # should it be TestRail .est ID: or TestRail test ID: ??
        case_re = re.compile(r"TestRail .est ID: \[?" + case_id)
        case_dependencies = self.search_bug_by_block(parent_bug_id).get("bugs")
        logging.warning(f"case_dependencies: {case_dependencies}")
        return [
            bug
            for bug in case_dependencies
            if case_re.search(bug.get("description", ""))
        ]

    def find_bugs_by_test_case_ids(self, case_ids: list[str], parent_bug_id: int = FUNCTIONAL_ROOT_METABUG):
        """
            Given a suite bug id and a test case idw, find all the test case bugs that are blocked on the suite bug.
            If no suite bug is provided, use the functional root meta bug.
        """
        if not case_ids:
            return []
        # should it be TestRail .est ID: or TestRail test ID: ??
        case_res = [re.compile(r"TestRail .est ID: \[?" + case_id) for case_id in case_ids]
        case_dependencies = self.search_bug_by_block(parent_bug_id).get("bugs")
        logging.warning(f"case_dependencies: {case_dependencies}")
        matching_bugs = []
        for case_re in case_res:
            matching_bugs += [
                bug
                for bug in case_dependencies
                if case_re.search(bug.get("description", ""))
        ]
        return matching_bugs
    def create_bug_structure(self, root_bug_id, content_payload):
        suite_bug_name = populate_template("suite", "title", content_payload)
        suite_metabugs = self.search_bug_by_block(root_bug_id).get("bugs")
        matching_suites = [
            bug
            for bug in suite_metabugs
            if f"(S{content_payload.get('suite_id')})" in (bug.get("summary", ""))
        ]
        if not matching_suites:
            logging.warning("not matching suite")
            suite_bug_body = populate_template("suite", "body", content_payload)
            suite_bug_id = self.create_blocking_bug(
                {
                    "summary": suite_bug_name,
                    "description": suite_bug_body,
                },
                root_bug_id,
            )
            # Indexing on results for get_bug and search_bug is necessary
            suite_bug = self.get_bug(suite_bug_id).get("bugs")[0]
        elif len(matching_suites) == 1:
            logging.warning(f"1 matching_suites: {matching_suites}")
            suite_bug = matching_suites[0]
            suite_bug_id = suite_bug.get("id")
        else:
            logging.warning("many suites")
            # TODO: is this case an error?
            suite_bug = matching_suites[0]
            suite_bug_id = suite_bug.get("id")

        case_params = []
        for case_ in content_payload.get("cases"):
            logging.warning(f"case {case_}")
            case_bug_name = populate_template("case", "title", case_ | content_payload)
            case_matches = self.find_bugs_by_test_case_id(str(case_.get('case_id')), suite_bug_id)
            logging.warning(f"matches {case_matches}")
            if not case_matches:
                logging.warning("not case matches")
                case_bug_body = populate_template(
                    "case", "body", case_ | content_payload
                )
                case_params.append(
                    {
                        "summary": case_bug_name,
                        "description": case_bug_body,
                    }
                )

        if case_params:
            logging.warning("case_params")
            self.create_blocking_bugs(case_params, suite_bug["id"])
