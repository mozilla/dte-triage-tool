import streamlit as st

from streamlit_kanban import kanban
from src.core.triage import Triage


def run():
    st.set_page_config(layout="wide")

    st.title("Test Case Triage Kanban Board")
    st.markdown("This tool helps Desktop Test Engineering triage test cases for future automation.")

    with st.sidebar:
        st.header("Triage Configuration")
        form_values = {'suite_id': st.text_input("Suite ID", "2054"), 'priority_id': st.text_input("Priority ID", "1"),
                       'automation_status': st.text_input("Automation Status", "1")}
        if st.button("Fetch Test Cases"):
            if all(form_values.values()):
                st.session_state.test_cases = fetch_test_cases(form_values['suite_id'], form_values['priority_id'], form_values['automation_status'])
                print(st.session_state.test_cases['cases'])
            else:
                st.warning("Please fill in all required fields.")

    # Main content area
    if "test_cases" in st.session_state:
        display_kanban_board(st.session_state.test_cases)
    else:
        st.info("Please configure the triage settings in the sidebar and click 'Fetch Test Cases'.")

def fetch_test_cases(suite_id, priority_id, automation_status):
    """
    Fetches test cases from TestRail based on the provided criteria.
    """
    triage_service = Triage()
    form_values = {
        "suite_id": int(suite_id),
        "priority_id": int(priority_id),
        "automation_status": int(automation_status)
    }
    return triage_service.tr_session.get_test_cases(17, form_values)

def display_kanban_board(test_cases):
    """
    Displays the Kanban board with the fetched test cases.
    """
    cols = [
        {
            "id": "test_cases_unorganized",
            "title": "Test Cases",
            "cards": [
                {"id": f"card-{testcase['id']}", "name": testcase['title'], "fields": ["Bug"], "color": f"#5550FF"} for testcase in test_cases.get('cases', [])
            ],
        },
        {
            "id": "test_cases_suitable",
            "title": "Automation Suitable Test Cases",
            "cards": [
            ],
        },
        {"id": "test_cases_unsuitable", "title": "Automation UnSuitable Test Cases", "cards": []},
    ]

    kanban(cols)