import os
import json
import streamlit as st
from streamlit_cookies_manager import CookieManager

from src.core.state import SessionState
from src.config.types import SessionKey
from src.UI.kanban import Kanban

COOKIE_PREFIX = "dte_triage_"
COOKIE_KEY = "session_state"

def load_session_from_cookies(cookies):
    """Load selected session_state keys from cookies into st.session_state."""
    raw = cookies.get(COOKIE_KEY)
    if not raw:
        return

    try:
        data = json.loads(raw)
    except Exception:
        return

    for key in SessionKey:
        name = key.value
        if name in data:
            st.session_state[name] = data[name]


def save_session_to_cookies(cookies):
    state_to_persist = {}
    for key in (
        SessionKey.FORM_VALUES,
        SessionKey.SEARCH_PARAMS,
        SessionKey.STATUS_MAP,
        SessionKey.INITIAL_BOARD,
    ):
        value = st.session_state.get(key.value)
        if value is not None:
            state_to_persist[key.value] = value

    cookies[COOKIE_KEY] = json.dumps(state_to_persist)
    cookies.save()


def run_app():
    cookies = CookieManager(
        prefix=COOKIE_PREFIX
    )
    if not cookies.ready():
        st.stop()
    load_session_from_cookies(cookies)

    kanban = Kanban()
    kanban.run()

    save_session_to_cookies(cookies)


if __name__ == "__main__":
    run_app()