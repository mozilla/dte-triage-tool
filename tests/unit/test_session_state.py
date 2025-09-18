class TestSessionState:
    def test_form_values_set_get_has_clear(self, session_state):
        assert session_state.get_form_values() is None
        assert session_state.has_form_values() is False

        vals = {
            "suite_id": 1,
            "priority_id": [(1, "Low")],
            "automation_status": [(2, "Suitable")],
        }
        session_state.set_form_values(vals)
        assert session_state.get_form_values() == vals
        assert session_state.has_form_values() is True

        session_state.clear_form_values()
        assert session_state.get_form_values() is None
        assert session_state.has_form_values() is False

    def test_priorities_set_get_has_clear(self, session_state):
        assert session_state.get_priorities() is None
        assert session_state.has_priorities() is False

        priorities = [
            {
                "id": 1,
                "priority": 1,
                "name": "Low",
                "short_name": "L",
                "is_default": False,
            }
        ]
        session_state.set_priorities(priorities)
        assert session_state.get_priorities() == priorities
        assert session_state.has_priorities() is True

        session_state.clear_priorities()
        assert session_state.get_priorities() is None
        assert session_state.has_priorities() is False

    def test_initial_board_set_get_has_clear(self, session_state):
        assert session_state.get_initial_board() is None
        assert session_state.has_initial_board() is False

        board = [{"id": "status-suitable", "title": "Status Suitable", "cards": []}]
        session_state.set_initial_board(board)
        assert session_state.get_initial_board() == board
        assert session_state.has_initial_board() is True

        session_state.clear_initial_board()
        assert session_state.get_initial_board() is None
        assert session_state.has_initial_board() is False

    def test_status_map_set_get_has_clear(self, session_state):
        assert session_state.get_status_map() is None
        assert session_state.has_status_map() is False

        status_map = {1: ("Status Untriaged", "Status Suitable")}
        session_state.set_status_map(status_map)
        assert session_state.get_status_map() == status_map
        assert session_state.has_status_map() is True

        session_state.clear_status_map()
        assert session_state.get_status_map() is None
        assert session_state.has_status_map() is False

    def test_clear_cache_removes_all_keys(self, session_state):
        session_state.set_form_values(
            {"suite_id": 1, "priority_id": [], "automation_status": []}
        )
        session_state.set_priorities(
            [
                {
                    "id": 1,
                    "priority": 1,
                    "name": "Low",
                    "short_name": "L",
                    "is_default": False,
                }
            ]
        )
        session_state.set_initial_board(
            [{"id": "status-suitable", "title": "Status Suitable", "cards": []}]
        )
        session_state.set_status_map({1: ("Status Untriaged", "Status Suitable")})

        assert session_state._state
        session_state.clear_cache()
        assert session_state._state == {}
