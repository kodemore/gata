import re
from datetime import date, datetime, time
from ipaddress import IPv4Address, IPv6Address
from typing import (
    Dict,
    FrozenSet,
    Iterable,
    List,
    Optional,
    Pattern,
    Sequence,
    Set,
    Tuple,
)

import pytest
from typing_extensions import Literal, TypedDict

from gata.dataclass.schema import map_meta_to_validator, map_type_to_validator, validate
from gata.errors import ValidationError
from tests.fixtures import Pet


def test_map_int_to_validator() -> None:
    validate = map_type_to_validator(int)

    assert 1 == validate(1)

    with pytest.raises(ValidationError):
        validate(None)


def test_map_str_to_validator() -> None:
    validate = map_type_to_validator(str)
    assert "abc" == validate("abc")

    with pytest.raises(ValidationError):
        validate(None)


def test_map_bool_to_validator() -> None:
    validate = map_type_to_validator(bool)
    assert True is validate(True)

    with pytest.raises(ValidationError):
        validate(None)


def test_map_float_to_validator() -> None:
    validate = map_type_to_validator(float)
    assert 1.23 == validate(1.23)

    with pytest.raises(ValidationError):
        validate(None)


def test_map_datetime_to_validator() -> None:
    validate = map_type_to_validator(datetime)

    assert datetime(year=2020, month=1, day=1, hour=1, minute=2, second=3) == validate(
        "2020-01-01T01:02:03"
    )
    with pytest.raises(ValidationError):
        validate(None)


def test_map_date_to_validator() -> None:
    validate = map_type_to_validator(date)

    assert date(year=2020, month=1, day=1) == validate("2020-01-01")
    with pytest.raises(ValidationError):
        validate(None)


def test_map_time_to_validator() -> None:
    validate = map_type_to_validator(time)

    assert time(hour=1, minute=2, second=3) == validate("01:02:03")
    with pytest.raises(ValidationError):
        validate(None)


def test_map_ipv4_address_to_validator() -> None:
    validate = map_type_to_validator(IPv4Address)

    assert IPv4Address("192.168.1.1") == validate("192.168.1.1")
    with pytest.raises(ValidationError):
        validate(None)


def test_map_ipv6_address_to_validator() -> None:
    validate = map_type_to_validator(IPv6Address)

    assert IPv6Address("2001:0db8:85a3:0000:0000:8a2e:0370:7334") == validate(
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
    with pytest.raises(ValidationError):
        validate(None)


def test_map_list_to_validator() -> None:
    validate = map_type_to_validator(list)

    assert [1, 2, 3] == validate([1, 2, 3])
    with pytest.raises(ValidationError):
        validate(None)


def test_map_set_to_validator() -> None:
    validate = map_type_to_validator(set)

    assert {1, 2, 3} == validate({1, 2, 3})
    with pytest.raises(ValidationError):
        validate(None)


def test_map_frozenset_to_validator() -> None:
    validate = map_type_to_validator(frozenset)

    assert frozenset({1, 2, 3}) == validate(frozenset({1, 2, 3}))
    with pytest.raises(ValidationError):
        validate(None)


def test_map_bytes_to_validator() -> None:
    validate = map_type_to_validator(bytes)

    assert b"abc" == validate(b"abc")

    with pytest.raises(ValidationError):
        validate(None)


def test_map_concrete_list_to_validator() -> None:
    validate = map_type_to_validator(List[date])

    assert [
        date(year=2020, month=1, day=1),
        date(year=2020, month=2, day=1),
    ] == validate(["2020-01-01", date(year=2020, month=2, day=1)])

    with pytest.raises(ValidationError):
        validate(None)


def test_map_concrete_tuple_to_validator() -> None:
    validate = map_type_to_validator(Tuple[date, bool, int])

    assert validate(("2020-01-01", "on", 1)) == (
        date(year=2020, month=1, day=1),
        True,
        1,
    )

    with pytest.raises(ValidationError):
        validate(None)


def test_map_concrete_set_to_validator() -> None:
    validate = map_type_to_validator(Set[date])

    assert validate({"2020-01-01", "2020-01-02"}) == {
        date(year=2020, month=1, day=1),
        date(year=2020, month=1, day=2),
    }

    with pytest.raises(ValidationError):
        validate(None)


def test_map_concrete_frozenset_to_validator() -> None:
    validate = map_type_to_validator(FrozenSet[date])

    assert validate(frozenset({"2020-01-01", "2020-01-02"})) == frozenset(
        [date(year=2020, month=1, day=1), date(year=2020, month=1, day=2)]
    )

    with pytest.raises(ValidationError):
        validate(None)


def test_map_concrete_iterable_to_validator() -> None:
    validate = map_type_to_validator(Iterable[int])

    assert validate([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        validate(None)


def test_map_concrete_sequence_to_validator() -> None:
    validate = map_type_to_validator(Sequence[int])

    assert validate([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        validate(None)


def test_map_concrete_dict_to_validator() -> None:
    validate = map_type_to_validator(Dict[str, int])

    assert validate({"a": 1, "b": 2, "c": 3}) == {"a": 1, "b": 2, "c": 3}

    with pytest.raises(ValidationError):
        validate(None)

    with pytest.raises(ValidationError):
        validate({"a": "b"})


def test_map_optional_type_to_validator() -> None:
    optional_int = map_type_to_validator(Optional[int])

    assert optional_int(None) is None
    assert optional_int(2) == 2

    with pytest.raises(ValidationError):
        optional_int("a")

    optional_list = map_type_to_validator(Optional[List[date]])

    assert optional_list(None) is None
    assert optional_list([]) == []
    assert optional_list(["2020-01-01"]) == [date(2020, 1, 1)]

    with pytest.raises(ValidationError):
        optional_list("aa")


def test_map_typed_dict_to_validator() -> None:
    class TestDict(TypedDict):
        name: str
        when: Optional[date]
        tags: List[str]

    validate = map_type_to_validator(TestDict)

    assert validate(TestDict(name="test", tags=["a", "b"])) == {
        "name": "test",
        "tags": ["a", "b"],
    }

    with pytest.raises(ValidationError):
        validate(TestDict(tags=["a", "b"]))

    with pytest.raises(ValidationError):
        validate(TestDict(name="test", tags=[1, "b"]))

    with pytest.raises(ValidationError):
        validate(TestDict(name="test", tags=["a", "b"], when="2020"))


def test_map_pattern_to_validator() -> None:
    validate = map_type_to_validator(Pattern)

    assert validate("[a-z]") == re.compile("[a-z]")

    with pytest.raises(ValidationError):
        validate("[?/")


def test_map_literal_to_validator() -> None:
    validate = map_type_to_validator(Literal["a", "b", "c"])

    assert validate("a") == "a"
    assert validate("c") == "c"

    with pytest.raises(ValidationError):
        validate("e")

    with pytest.raises(ValidationError):
        validate(None)


def test_map_meta_to_validator() -> None:
    validate_email_str = map_meta_to_validator(str, {"format": "email", "min": 8})

    assert validate_email_str("test@test.com") == "test@test.com"
    assert validate_email_str(None) is None

    with pytest.raises(ValidationError):
        validate_email_str("eeeeeeeee")

    with pytest.raises(ValidationError):
        validate_email_str("a@a.com")

    validate_min_max = map_meta_to_validator(int, {"min": 0, "max": 4})

    assert validate_min_max(1) == 1
    assert validate_min_max(0) == 0
    assert validate_min_max(4) == 4
    assert validate_min_max(None) is None

    with pytest.raises(ValidationError):
        validate_min_max(-1)


def test_validate_dataclass() -> None:
    assert validate(
        {
            "name": "Boo",
            "created_at": "2020-01-01T20:20:10",
            "tags": [],
            "favourites": [],
            "status": 0,
            "age": 10,
        },
        Pet,
    )

    try:
        validate({}, Pet)
    except ValidationError as error:
        assert error.context.get("field_name") == "name"
