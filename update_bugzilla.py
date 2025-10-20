from dotenv import load_dotenv
from src.core.integrations.bugzilla_integration import Bugzilla
from os import environ
import sys
import json

FUNCTIONAL_ROOT_METABUG = 1976270

if __name__ == "__main__":
    load_dotenv()
    bz = Bugzilla(environ.get("BUGZILLA_BASE_URL"))
    payload = {}
    for session_file in sys.argv[1:]:
        with open(session_file) as fh:
            session_payload = json.load(fh)
            session_suite_id = session_payload.get('suite_id')
            if payload.get(session_suite_id):
                payload.get(session_suite_id).get('cases').extend(session_payload.get('cases'))
            else:
                payload[session_suite_id] = session_payload

    for suite_payload in payload.values():
        print(suite_payload)
        bz.create_bug_structure(FUNCTIONAL_ROOT_METABUG, suite_payload)
