import pytest

from gata.errors import InvalidTypeError, ValidationError
from gata.types import *


def test_one_of() -> None:
    string_or_number = OneOf[String, Number]

    string_or_number.validate("test string")
    string_or_number.validate(12)
    string_or_number.validate(12.32)
    string_or_number.validate("12.322")


def test_fail_one_of_instantiation() -> None:
    with pytest.raises(InvalidTypeError):
        OneOf[String]

    with pytest.raises(InvalidTypeError):
        OneOf[1, 2]


def test_fail_invalid_value_one_of() -> None:
    string_or_number = OneOf[String, Number]
    with pytest.raises(ValidationError):
        string_or_number.validate([])
