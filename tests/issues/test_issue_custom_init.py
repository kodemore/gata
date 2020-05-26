from gata import dataclass
from uuid import uuid4
import pytest


def test_custom_init_with_validator() -> None:
    @dataclass
    class TestInit:
        id: str
        field_a: str
        field_b: int
        post_init: bool = False

        def __init__(self, payload: list):
            self.id = str(uuid4())
            self.field_a = payload[0]
            self.field_b = payload[1]

        def __post_init__(self) -> None:
            self.post_init = True

    instance = TestInit(["a", 1])
    assert instance.field_a == "a"
    assert instance.field_b == 1
    assert instance.post_init

    with pytest.raises(ValueError):
        TestInit([1, 2])


def test_custom_init_for_frozen_dataclass() -> None:

    @dataclass(frozen=True)
    class TestFrozenInit:
        field_a: str
        field_b: int

        def __init__(self, payload: list):
            self.field_a = payload[0]
            self.field_b = payload[1]

    instance = TestFrozenInit(["a", 1])
    assert instance.field_a == "a"
    assert instance.field_b == 1

    instance_b = TestFrozenInit(["b", 2])
    assert instance_b.field_a == "b"
    assert instance_b.field_b == 2
