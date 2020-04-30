import pytest

from gata.schema import build_schema
from gata.dataclass import field


def test_schema_int_type():
    class TestClass:
        property: int

    schema = build_schema(TestClass)

    assert schema["property"].type is int
    assert schema["property"].validate(12)

    with pytest.raises(ValueError):
        schema["property"].validate("12")


def test_schema_bool_type():
    class TestClass:
        property: bool

    schema = build_schema(TestClass)

    assert schema["property"].type is bool
    assert schema["property"].validate("on")
    assert not schema["property"].validate(False)

