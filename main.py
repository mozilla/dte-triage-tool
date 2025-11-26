from src.UI.kanban import Kanban
from src.core.state import SessionState


def run_app():
    # Initialize session state wrapper
    session = SessionState()

    # Hydrate state from local storage
    session.sync_all_from_storage()

    kanban = Kanban()
    kanban.run()

    # Persist state to local storage
    session.sync_all_to_storage()

if __name__ == "__main__":
    run_app()