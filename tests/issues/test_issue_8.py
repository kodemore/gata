from uuid import uuid4
from gata import dataclass, field


def test_issue_8() -> None:

    @dataclass()
    class TestDataclass:
        _id: str = field(init=False)

        def __post_init__(self):
            self._id = str(uuid4())

        @property
        def id(self):
            return self._id

    instance_1 = TestDataclass()
    instance_2 = TestDataclass()

    assert instance_1 != instance_2

    assert TestDataclass.validate({}) is None
