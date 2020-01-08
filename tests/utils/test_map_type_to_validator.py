import pytest
from typing import Callable, Union
from gata.utils.map_type_to_validator import map_type_to_validator
from gata.validators import validate_integer
from gata.validators import validate_boolean
from gata.validators import validate_number
from gata.validators import validate_string
from enum import Enum
from typing import List, Set, Optional
from datetime import datetime, date, time


@pytest.mark.parametrize(
    "base_type, expected_validator",
    [
        (int, validate_integer),
        (bool, validate_boolean),
        (float, validate_number),
        (str, validate_string),
    ],
)
def test_validate_base_types(base_type, expected_validator: Callable) -> None:
    assert map_type_to_validator(base_type) == expected_validator


def test_validate_enum() -> None:
    class TestEnum(Enum):
        ONE = 1
        TWO = 2
        THREE = 3

    validate = map_type_to_validator(TestEnum)

    assert validate(1)
    assert validate(2)
    assert validate(3)

    with pytest.raises(ValueError):
        validate(4)


def test_validate_concrete_list() -> None:
    validate = map_type_to_validator(List[str])

    assert validate(["a", "b", "c"])

    with pytest.raises(ValueError):
        validate([1, 2])

    with pytest.raises(ValueError):
        validate("a")


def test_validate_concrete_set() -> None:
    validate = map_type_to_validator(Set[str])

    assert validate(["a", "b", "c"])

    with pytest.raises(ValueError):
        validate("a")

    with pytest.raises(ValueError):
        validate([1, 2, 3])

    with pytest.raises(ValueError):
        validate(["a", 3])

    with pytest.raises(ValueError):
        validate(["a", "a"])


def test_validate_union() -> None:
    validate = map_type_to_validator(Union[str, int])

    assert validate(1)
    assert validate("2")

    with pytest.raises(ValueError):
        validate(True)

    with pytest.raises(ValueError):
        validate([1])


def test_validate_optional() -> None:
    validate = map_type_to_validator(Optional[int])

    assert validate(None)
    assert validate(1)

    with pytest.raises(ValueError):
        validate("")


def test_validate_datetime() -> None:
    validate = map_type_to_validator(datetime)

    assert validate("2019-10-10 10:10:10")

    with pytest.raises(ValueError):
        validate("2019-10-10")


def test_validate_date() -> None:
    validate = map_type_to_validator(date)

    assert validate("2019-10-10")

    with pytest.raises(ValueError):
        validate("2019-10-10 10:10:10")


def test_validate_time() -> None:
    validate = map_type_to_validator(time)

    assert validate("10:10:10")

    with pytest.raises(ValueError):
        validate("2019-10-10 10:10:10")
