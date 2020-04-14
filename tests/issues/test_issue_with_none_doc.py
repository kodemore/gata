from gata import serialisable


def test_issue_with_none_doc() -> None:
    @serialisable
    class Event:
        id: str
        name: str

    class ChildEvent(Event):
        def __init__(self, event_id: str, name: str):
            self.id = event_id
            self.name = name

    event = ChildEvent("12", "child-event")

    assert event.serialise() == {  # type: ignore
        "id": "12",
        "name": "child-event",
    }
