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
            payload |= json.load(fh)

    print(payload)
    bz.create_bug_structure(FUNCTIONAL_ROOT_METABUG, payload)
