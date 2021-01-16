from hfsm import Event


class TestEvent:

    def test_event_constructor(self):
        event = Event("event")
        assert event.name == "event"

    def test_equality(self):
        event1 = Event("event")
        event2 = Event("event")
        assert event1 == event2
