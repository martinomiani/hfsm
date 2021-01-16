from hfsm import State, StateMachine, ExitState
from unittest.mock import MagicMock


class TestState:

    def test_constructor_default(self):
        state = State("state")
        assert state.name == "state"
        assert state.child_sm is None
        assert not state.has_child_sm()

    def test_constructor_with_child(self):
        child_state_machine = StateMachine("state_machine")
        state = State("state", child_state_machine)
        assert state.name == "state"
        assert state.child_sm is not None
        assert state.has_child_sm()

    def test_equality(self):
        state1 = State("state")
        state2 = State("state")
        assert state1 == state2

    def test_set_child_sm(self):
        child_state_machine = StateMachine("state_machine")
        state = State("state")
        assert state.child_sm is None
        assert not state.has_child_sm()
        state.set_child_sm(child_state_machine)
        assert state.child_sm is not None
        assert state.has_child_sm()

    def test_set_parent_sm(self):
        parent_state_machine = StateMachine("state_machine")
        state = State("state")
        assert state.parent_sm is None
        state.set_parent_sm(parent_state_machine)
        assert state.parent_sm is not None

    def test_on_entry(self):
        callback = MagicMock()
        state = State("state")
        state.on_entry(callback)
        state.start("data")
        callback.assert_called_once_with("data")

    def test_on_exit(self):
        callback = MagicMock()
        state = State("state")
        state.on_exit(callback)
        state.start("data")
        state.stop("data")
        callback.assert_called_once_with("data")


class TestExitState:

    def test_exit_state_constructor_default(self):
        exit_state = ExitState()
        assert exit_state.name == "NormalExitState"
        assert exit_state.status == "Normal"

    def test_exit_state_constructor_with_status(self):
        exit_state = ExitState("Error")
        assert exit_state.name == "ErrorExitState"
        assert exit_state.status == "Error"
