from hfsm import NormalTransition, SelfTransition, NullTransition, \
    State, Event
from unittest.mock import MagicMock


class TestTransition:

    def test_normal_transition_constructor(self):
        source_state = State("source")
        destination_state = State("destination")
        event = Event("event")
        transition = NormalTransition(source_state, destination_state, event)
        assert transition.event == event
        assert transition.source_state == source_state
        assert transition.destination_state == destination_state

    def test_self_transition_constructor(self):
        source_state = State("source")
        event = Event("event")
        transition = SelfTransition(source_state, event)
        assert transition.event == event
        assert transition.source_state == source_state
        assert transition.destination_state == source_state

    def test_null_transition_constructor(self):
        source_state = State("source")
        event = Event("event")
        transition = NullTransition(source_state, event)
        assert transition.event == event
        assert transition.source_state == source_state
        assert transition.destination_state == source_state

    def test_normal_transition_no_condition(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        destination_state = State("destination")
        destination_state.on_entry(entry_callback)
        event = Event("event")
        transition = NormalTransition(source_state, destination_state, event)
        transition("data")
        entry_callback.assert_called_once_with("data")
        exit_callback.assert_called_once_with("data")

    def test_normal_transition_condition_true(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        destination_state = State("destination")
        destination_state.on_entry(entry_callback)
        event = Event("event")
        transition = NormalTransition(source_state, destination_state, event)
        condition_callback = MagicMock(return_value=True)
        transition.add_condition(condition_callback)
        transition("data")
        entry_callback.assert_called_once_with("data")
        exit_callback.assert_called_once_with("data")
        condition_callback.assert_called_once_with("data")

    def test_normal_transition_condition_false(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        destination_state = State("destination")
        destination_state.on_entry(entry_callback)
        event = Event("event")
        transition = NormalTransition(source_state, destination_state, event)
        condition_callback = MagicMock(return_value=False)
        transition.add_condition(condition_callback)
        transition("data")
        entry_callback.assert_not_called()
        exit_callback.assert_not_called()
        condition_callback.assert_called_once_with("data")

    def test_normal_transition_action(self):
        source_state = State("source")
        destination_state = State("destination")
        event = Event("event")
        transition = NormalTransition(source_state, destination_state, event)
        condition_callback = MagicMock(return_value=True)
        action_callback = MagicMock()
        transition.add_condition(condition_callback)
        transition.add_action(action_callback)
        transition("data")
        condition_callback.assert_called_once_with("data")
        action_callback.assert_called_once_with("data")

    def test_self_transition_no_condition(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        source_state.on_entry(entry_callback)
        event = Event("event")
        transition = SelfTransition(source_state, event)
        transition("data")
        entry_callback.assert_called_once_with("data")
        exit_callback.assert_called_once_with("data")

    def test_self_transition_condition_true(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        source_state.on_entry(entry_callback)
        event = Event("event")
        transition = SelfTransition(source_state, event)
        condition_callback = MagicMock(return_value=True)
        transition.add_condition(condition_callback)
        transition("data")
        entry_callback.assert_called_once_with("data")
        exit_callback.assert_called_once_with("data")
        condition_callback.assert_called_once_with("data")

    def test_self_transition_condition_false(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        source_state.on_entry(entry_callback)
        event = Event("event")
        transition = SelfTransition(source_state, event)
        condition_callback = MagicMock(return_value=False)
        transition.add_condition(condition_callback)
        transition("data")
        entry_callback.assert_not_called()
        exit_callback.assert_not_called()
        condition_callback.assert_called_once_with("data")

    def test_self_transition_action(self):
        source_state = State("source")
        event = Event("event")
        transition = SelfTransition(source_state, event)
        condition_callback = MagicMock(return_value=True)
        action_callback = MagicMock()
        transition.add_condition(condition_callback)
        transition.add_action(action_callback)
        transition("data")
        condition_callback.assert_called_once_with("data")
        action_callback.assert_called_once_with("data")

    def test_null_transition_no_condition(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        source_state.on_entry(entry_callback)
        event = Event("event")
        transition = NullTransition(source_state, event)
        transition("data")
        entry_callback.assert_not_called()
        exit_callback.assert_not_called()

    def test_null_transition_condition_true(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        source_state.on_entry(entry_callback)
        event = Event("event")
        transition = NullTransition(source_state, event)
        condition_callback = MagicMock(return_value=True)
        transition.add_condition(condition_callback)
        transition("data")
        entry_callback.assert_not_called()
        exit_callback.assert_not_called()
        condition_callback.assert_called_once_with("data")

    def test_null_transition_condition_false(self):
        entry_callback = MagicMock()
        exit_callback = MagicMock()
        source_state = State("source")
        source_state.on_exit(exit_callback)
        source_state.on_entry(entry_callback)
        event = Event("event")
        transition = NullTransition(source_state, event)
        condition_callback = MagicMock(return_value=False)
        transition.add_condition(condition_callback)
        transition("data")
        entry_callback.assert_not_called()
        exit_callback.assert_not_called()
        condition_callback.assert_called_once_with("data")

    def test_null_transition_action(self):
        source_state = State("source")
        event = Event("event")
        transition = NullTransition(source_state, event)
        condition_callback = MagicMock(return_value=True)
        action_callback = MagicMock()
        transition.add_condition(condition_callback)
        transition.add_action(action_callback)
        transition("data")
        condition_callback.assert_called_once_with("data")
        action_callback.assert_called_once_with("data")
