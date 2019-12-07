import pytest

from gata.errors import InvalidTypeError
from gata.types import *


def test_any_of() -> None:
    string_or_number = AnyOf[String, Number]

    string_or_number.validate("test string")
    string_or_number.validate(12)
    string_or_number.validate(12.32)
    string_or_number.validate("12.322")


def test_fail_any_of_instantiation() -> None:
    with pytest.raises(InvalidTypeError):
        AnyOf[String]

    with pytest.raises(InvalidTypeError):
        AnyOf[1, 2]
