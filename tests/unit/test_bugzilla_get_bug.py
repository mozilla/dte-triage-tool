from src.core.integrations.bugzilla_integration import Bugzilla

from dotenv import load_dotenv
from os import environ
import logging

BUG_ID = 1935731

def test_bugzilla_get_bug():
    load_dotenv()
    bz = Bugzilla(environ.get("BUGZILLA_BASE_URL"))
    response = bz.get_bug(BUG_ID)

    logging.info(response)
