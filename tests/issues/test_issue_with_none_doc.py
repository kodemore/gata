from gata import dataclass


def test_issue_with_none_doc() -> None:
    @dataclass
    class Event:
        id: str
        name: str = "Bob"

    class ChildEvent(Event):
        def __init__(self, event_id: str, name: str):
            self.id = event_id
            self.name = name

    event = ChildEvent("12", "child-event")

    assert event.serialise() == {  # type: ignore
        "id": "12",
        "name": "child-event",
    }
