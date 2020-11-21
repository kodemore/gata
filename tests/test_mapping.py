import base64
from datetime import date, datetime, time, timedelta
from ipaddress import IPv4Address, IPv6Address
import re
from typing import List, Pattern, Tuple
from uuid import UUID

import pytest

from gata.dataclasses import field, build_schema
from gata import mapping


def test_schema_int_type() -> None:
    class TestClass:
        property: int

    schema = build_schema(TestClass)

    assert "property" in schema
    assert schema["property"].type is int
    assert schema["property"].validate(12)

    with pytest.raises(ValueError):
        schema["property"].validate("12")


def test_schema_bool_type() -> None:
    class TestClass:
        property: bool

    schema = build_schema(TestClass)

    assert schema["property"].type is bool
    assert schema["property"].validate("on")
    assert not schema["property"].validate(False)

    with pytest.raises(ValueError):
        schema["property"].validate(32)


def test_schema_float_type() -> None:
    class TestClass:
        property: float

    schema = build_schema(TestClass)

    assert schema["property"].type is float
    assert schema["property"].validate(12.21) == 12.21
    assert schema["property"].validate(0.0) == 0.0

    with pytest.raises(ValueError):
        schema["property"].validate(1)


def test_schema_string_type() -> None:
    class TestClass:
        property: str

    schema = build_schema(TestClass)

    assert schema["property"].type is str
    assert schema["property"].validate("test") == "test"

    with pytest.raises(ValueError):
        schema["property"].validate(True)


def test_schema_date_type() -> None:
    class TestClass:
        property: date

    schema = build_schema(TestClass)

    assert schema["property"].type is date
    assert schema["property"].validate("2020-10-20") == date(
        year=2020, month=10, day=20
    )

    with pytest.raises(ValueError):
        schema["property"].validate(123)


def test_schema_datetime_type() -> None:
    class TestClass:
        property: datetime

    schema = build_schema(TestClass)

    assert schema["property"].type is datetime
    assert schema["property"].validate("2020-10-20 10:21:59") == datetime(
        year=2020, month=10, day=20, hour=10, minute=21, second=59
    )

    with pytest.raises(ValueError):
        schema["property"].validate(123)


def test_schema_time_type() -> None:
    class TestClass:
        property: time

    schema = build_schema(TestClass)

    assert schema["property"].type is time
    assert schema["property"].validate("10:21:59") == time(
        hour=10, minute=21, second=59
    )

    with pytest.raises(ValueError):
        schema["property"].validate(123)


def test_schema_duration_type() -> None:
    class TestClass:
        property: timedelta

    schema = build_schema(TestClass)

    assert schema["property"].type is timedelta
    assert schema["property"].validate("P2DT5H") == timedelta(days=2, hours=5)

    with pytest.raises(ValueError):
        schema["property"].validate(123)


def test_schema_pattern_type() -> None:
    class TestClass:
        property: Pattern[str]

    schema = build_schema(TestClass)

    assert schema["property"].type is Pattern[str]
    assert schema["property"].validate("a-z") == re.compile("a-z")

    with pytest.raises(ValueError):
        schema["property"].validate(123)


def test_schema_ipv6_address_type() -> None:
    class TestClass:
        property: IPv6Address

    schema = build_schema(TestClass)

    assert schema["property"].type is IPv6Address
    assert schema["property"].validate("1200:0000:AB00:1234:0000:2552:7777:1313")

    with pytest.raises(ValueError):
        schema["property"].validate("aaa")


def test_schema_ipv4_address_type() -> None:
    class TestClass:
        property: IPv4Address

    schema = build_schema(TestClass)

    assert schema["property"].type is IPv4Address
    assert schema["property"].validate("127.0.0.1")

    with pytest.raises(ValueError):
        schema["property"].validate("aaa")


def test_schema_uuid_type() -> None:
    class TestClass:
        property: UUID

    schema = build_schema(TestClass)

    assert schema["property"].type is UUID
    assert schema["property"].validate("bb2e4878-4bb2-440d-90ef-ba2724c1e8c2")

    with pytest.raises(ValueError):
        schema["property"].validate("aaa")


def test_schema_object_id_type() -> None:
    try:
        from bson import ObjectId
    except ImportError:
        pytest.skip("Bson not installed")

    class TestClass:
        property: ObjectId

    schema = build_schema(TestClass)

    assert schema["property"].type is ObjectId
    assert schema["property"].validate("507f1f77bcf86cd799439011")

    with pytest.raises(ValueError):
        schema["property"].validate("aaa")


def test_schema_bytes_and_bytes_array_type() -> None:
    class TestClass:
        property: bytes

    schema = build_schema(TestClass)

    assert schema["property"].type is bytes
    assert (
        schema["property"].validate(base64.b64encode(b"test bytes").decode("utf8"))
        == b"test bytes"
    )

    with pytest.raises(ValueError):
        schema["property"].validate("aaa")


def test_schema_simple_list_type() -> None:
    class TestClass:
        property: list

    schema = build_schema(TestClass)
    assert schema["property"].type is list

    assert schema["property"].validate([1, 2, 1.0, 2.0, "a", "b", True, False])

    with pytest.raises(ValueError):
        schema["property"].validate("non list")


def test_schema_typing_list_type() -> None:
    class TestClass:
        property: List

    schema = build_schema(TestClass)
    assert schema["property"].type is List

    assert schema["property"].validate([1, 2, 1.0, 2.0, "a", "b", True, False])

    with pytest.raises(ValueError):
        schema["property"].validate("non list")


def test_schema_typed_list_type() -> None:
    class TestClass:
        property: List[int] = field(maximum=10)

    schema = build_schema(TestClass)
    assert schema["property"].type is List[int]

    assert schema["property"].validate([1, 2, 3, 4])

    with pytest.raises(ValueError):
        schema["property"].validate([1, 2, True])


def test_schema_typed_list_type_with_items() -> None:
    class TestClass:
        property: List[int] = field(maximum=10, items={"minimum": 1, "maximum": 4})

    schema = build_schema(TestClass)
    assert schema["property"].type is List[int]

    assert schema["property"].validate([1, 2, 3, 4])

    with pytest.raises(ValueError):
        schema["property"].validate([1, 2, 5])


def test_boolean_type() -> None:
    test = mapping.BooleanMapping()

    assert test.serialise(True)
    assert not test.serialise(False)
    assert test.deserialise("on")
    assert not test.deserialise("off")


def test_integer_type() -> None:
    test = mapping.IntegerMapping()

    assert test.serialise(12) == 12
    assert test.deserialise(12) == 12
    assert test.validate(12) == 12

    with pytest.raises(ValueError):
        test.validate("12")

    min_max_test = mapping.IntegerMapping(minimum=4, maximum=12)
    assert min_max_test.validate(5) == 5

    with pytest.raises(ValueError):
        min_max_test.validate(2)

    with pytest.raises(ValueError):
        min_max_test.validate(13)


def test_float_type() -> None:
    test = mapping.FloatMapping()

    assert test.serialise(12.0) == 12.0
    assert test.deserialise(12.0) == 12.0
    assert test.validate(12.0) == 12.0

    with pytest.raises(ValueError):
        test.validate(1)

    min_max_test = mapping.FloatMapping(minimum=4.0, maximum=12.0)
    assert min_max_test.validate(5.0) == 5.0

    with pytest.raises(ValueError):
        min_max_test.validate(2.0)

    with pytest.raises(ValueError):
        min_max_test.validate(13.0)


def test_string_type() -> None:
    test = mapping.StringMapping()

    assert test.serialise("test word") == "test word"
    assert test.deserialise("test word") == "test word"
    assert test.validate("test word") == "test word"

    with pytest.raises(ValueError):
        test.validate(1)

    min_max_test = mapping.StringMapping(minimum=4, maximum=12)
    assert min_max_test.validate("test") == "test"

    with pytest.raises(ValueError):
        min_max_test.validate("abc")

    with pytest.raises(ValueError):
        min_max_test.validate("too long to be valid for this test")

    format_test = mapping.StringMapping(format="email")

    assert format_test.validate("some@email.com") == "some@email.com"
    with pytest.raises(ValueError):
        format_test.validate("not an email")

    pattern_test = mapping.StringMapping(pattern="[a-z]+")
    assert pattern_test.validate("abc") == "abc"

    with pytest.raises(ValueError):
        pattern_test.validate("ab1")


def test_set_type() -> None:
    test_type = mapping.SetMapping()

    assert test_type.validate({1, 2, 3})
    assert test_type.serialise({1, 2, 3}) == [1, 2, 3]
    assert test_type.deserialise([1, 2, 3]) == {1, 2, 3}


def test_tuple_type() -> None:
    class TestTuple:
        property: Tuple[int, ...]

    schema = build_schema(TestTuple)
    assert schema["property"].type is Tuple[int, ...]

    assert schema["property"].validate((1, 2, 3, 4))

    with pytest.raises(ValueError):
        schema["property"].validate((1, 2, 5, "a"))

