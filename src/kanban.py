import streamlit as st

from streamlit_kanban import kanban

from src.core.intergrations.controllers.triage_form import TriageFormController
from src.core.util import Util
from src.core.types import FormValues

def run():
    st.title("Test Case Triage Kanban Board")
    st.markdown("This tool helps Desktop Test Engineering triage test cases for future automation.")
    form_controller = TriageFormController()
    with st.sidebar:
        st.header("Triage Configuration")
        form_values: FormValues = form_controller.set_inputs()
        if st.button("Fetch Test Cases"):
            ok, msg = form_controller.query_and_save(form_values)
            if not ok:
                st.warning(msg)
            else:
                st.success("Test cases fetched.")


    # Main content area
    if form_controller.state.has_test_cases():
        display_kanban_board(form_controller.state.get_test_cases())
    else:
        st.info("Please configure the triage settings in the sidebar and click 'Fetch Test Cases'.")



def display_kanban_board(test_cases):
    """
    Displays the Kanban board with the fetched test cases.
    """
    cols = [
        {
            "id": "test_cases_unorganized",
            "title": "Test Cases",
            "cards": [
                {"id": f"card-{testcase['id']}", "name": testcase['title'], "fields": ["Bug"], "color": Util.priority_color(testcase['priority_id'])} for testcase in test_cases.get('cases', [])
            ],
        },
        {
            "id": "test_cases_suitable",
            "title": "Automation Suitable",
            "cards": [
            ],
        },
        {"id": "test_cases_unsuitable", "title": "Automation Unsuitable", "cards": []},
    ]
    if test_cases:
        kanban(cols)
    else:
        st.info("No test cases found.\nChange search criteria and retry.")