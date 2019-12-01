from typing import Any

from gata.types import Type


def test_can_extend_base_type():
    class TestType(Type):
        def validate(self, value: Any) -> None:
            pass

    test_type_instance = TestType()

    assert isinstance(test_type_instance, TestType)
    assert isinstance(test_type_instance, Type)

    sub_instance = test_type_instance()

    assert isinstance(sub_instance, TestType)
    assert isinstance(sub_instance, Type)
