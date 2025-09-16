import os
import streamlit.components.v1 as components

_RELEASE = os.path.exists(os.path.join(os.path.dirname(__file__), "build"))

if not _RELEASE:
    # if release mode, UI is running on the server otherwise UI is built locally.
    _component_func = components.declare_component(
        "kanban",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "build")
    _component_func = components.declare_component("kanban", path=build_dir)

def kanban(columns, key=None):
    """
    Displays the kanban component.
    """
    component_value = _component_func(columns=columns, key=key)
    return component_value
