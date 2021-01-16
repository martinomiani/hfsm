from hfsm import State, StateMachine, ExitState, Event
from unittest.mock import MagicMock
import pytest


class TestStateMachine:

    def test_sm_constructor(self):
        state_machine = StateMachine("sm")
        exit_state = ExitState()
        assert state_machine.name == "sm"
        assert state_machine.current_state is None
        assert state_machine.exit_state == exit_state

    def test_equality(self):
        state_machine1 = StateMachine("sm")
        state_machine2 = StateMachine("sm")
        assert state_machine1 == state_machine2

    def test_without_initial_state(self):
        state_machine = StateMachine("sm")
        with pytest.raises(ValueError):
            state_machine.start("data")

    def test_with_initial_state(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        entry_cb = MagicMock()
        initial_state.on_entry(entry_cb)
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.start("data")
        assert state_machine.current_state == initial_state
        entry_cb.assert_called_once_with("data")
        assert state_machine.is_running()

    def test_add_same_state_twice(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        state_machine.add_state(initial_state, initial_state=True)
        with pytest.raises(ValueError):
            state_machine.add_state(initial_state)

    def test_transition_with_invalid_event(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        second_state = State("second_state")
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        assert state_machine.add_transition(initial_state,
                                            second_state, event) is None

    def test_transition_with_valid_event(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        second_state = State("second_state")
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        state_machine.add_event(event)
        assert state_machine.add_transition(initial_state,
                                            second_state, event) is not None

    def test_self_transition_with_invalid_event(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        assert state_machine.add_self_transition(initial_state, event) is None

    def test_self_transition_with_valid_event(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_event(event)
        assert state_machine.add_self_transition(initial_state,
                                                 event) is not None

    def test_null_transition_with_invalid_event(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        assert state_machine.add_null_transition(initial_state,
                                                 event) is None

    def test_null_transition_with_valid_event(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_event(event)
        assert state_machine.add_null_transition(initial_state,
                                                 event) is not None

    def test_event_trigger(self):
        state_machine = StateMachine("sm")
        exit_cb = MagicMock()
        entry_cb = MagicMock()
        initial_state = State("initial_state")
        second_state = State("second_state")
        initial_state.on_exit(exit_cb)
        second_state.on_entry(entry_cb)
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        state_machine.add_event(event)
        state_machine.add_transition(initial_state, second_state, event)
        state_machine.start("data")
        exit_cb.assert_not_called()
        entry_cb.assert_not_called()
        state_machine.trigger_event(event, "data")
        exit_cb.assert_called_once_with("data")
        entry_cb.assert_called_once_with("data")

    def test_event_trigger_before_starting(self):
        state_machine = StateMachine("sm")
        exit_cb = MagicMock()
        entry_cb = MagicMock()
        initial_state = State("initial_state")
        second_state = State("second_state")
        initial_state.on_exit(exit_cb)
        second_state.on_entry(entry_cb)
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        state_machine.add_event(event)
        state_machine.add_transition(initial_state, second_state, event)
        with pytest.raises(ValueError):
            state_machine.trigger_event(event, "data")

    def test_event_trigger_no_initial_state(self):
        state_machine = StateMachine("sm")
        exit_cb = MagicMock()
        entry_cb = MagicMock()
        initial_state = State("initial_state")
        second_state = State("second_state")
        initial_state.on_exit(exit_cb)
        second_state.on_entry(entry_cb)
        event = Event("event")
        state_machine.add_state(initial_state)
        state_machine.add_state(second_state)
        state_machine.add_event(event)
        state_machine.add_transition(initial_state, second_state, event)
        with pytest.raises(ValueError):
            state_machine.trigger_event(event, "data")

    def test_event_trigger_propagate_but_no_child_sm(self):
        state_machine = StateMachine("sm")
        exit_cb = MagicMock()
        entry_cb = MagicMock()
        initial_state = State("initial_state")
        second_state = State("second_state")
        initial_state.on_exit(exit_cb)
        second_state.on_entry(entry_cb)
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        state_machine.add_event(event)
        state_machine.add_transition(initial_state, second_state, event)
        state_machine.start("data")
        exit_cb.assert_not_called()
        entry_cb.assert_not_called()
        state_machine.trigger_event(event, "data", propagate=True)
        # no child fsm in current state, so the event is caught in this fsm
        assert state_machine.current_state == second_state

    @staticmethod
    def create_child_fsm():
        state_machine = StateMachine("child_sm")
        exit_cb = MagicMock()
        entry_cb = MagicMock()
        initial_state = State("child_initial_state")
        second_state = State("child_second_state")
        initial_state.on_exit(exit_cb)
        second_state.on_entry(entry_cb)
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        state_machine.add_event(event)
        state_machine.add_transition(initial_state, second_state, event)

        return state_machine

    def test_event_trigger_propagate_with_child_sm(self):
        state_machine = StateMachine("sm")
        exit_cb = MagicMock()
        entry_cb = MagicMock()
        initial_state = State("initial_state")
        second_state = State("second_state")
        initial_state.on_exit(exit_cb)
        second_state.on_entry(entry_cb)
        initial_state.set_child_sm(self.create_child_fsm())
        event = Event("event")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        state_machine.add_event(event)
        state_machine.add_transition(initial_state, second_state, event)
        state_machine.start("data")
        exit_cb.assert_not_called()
        entry_cb.assert_not_called()
        state_machine.trigger_event(event, "data", propagate=True)
        # child fsm in current state, so the event is caught in child fsm
        assert state_machine.current_state == initial_state
        assert initial_state.child_sm.current_state.name == \
               "child_second_state"

    def test_exit_callback(self):
        exit_sm_cb = MagicMock()
        state_machine = StateMachine("sm")
        state_machine.on_exit(exit_sm_cb)
        initial_state = State("initial_state")
        second_state = State("second_state")
        exit_state_error = ExitState("Error")
        event = Event("event")
        error_event = Event("error")
        state_machine.add_state(initial_state, initial_state=True)
        state_machine.add_state(second_state)
        state_machine.add_state(exit_state_error)
        state_machine.add_event(event)
        state_machine.add_event(error_event)
        state_machine.add_transition(initial_state, second_state, event)
        state_machine.add_transition(second_state, exit_state_error,
                                     error_event)
        state_machine.start("data")
        assert state_machine.current_state == initial_state
        state_machine.trigger_event(event, "data")
        assert state_machine.current_state == second_state
        state_machine.trigger_event(error_event, "data")
        assert state_machine.current_state == exit_state_error
        exit_sm_cb.assert_called_once_with(exit_state_error, "data")

    def test_stop_before_starting(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        state_machine.add_state(initial_state, initial_state=True)
        with pytest.raises(ValueError):
            state_machine.stop("data")

    def test_stop_no_initial_state(self):
        state_machine = StateMachine("sm")
        initial_state = State("initial_state")
        state_machine.add_state(initial_state)
        with pytest.raises(ValueError):
            state_machine.stop("data")
