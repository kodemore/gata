import pytest

from gata.errors import InvalidLengthError
from gata.types import *


def test_can_instantiate():
    test_instance = Array()
    assert test_instance.validate([]) is None


def test_validate_items():
    test_instance = Array[String]
    assert test_instance.validate(["test", "strings", "to", "validate"]) is None


def test_validate_capacity():
    test_instance = Array(min_length=1, max_length=3)
    assert test_instance.validate([1, 2]) is None

    with pytest.raises(InvalidLengthError):
        test_instance.validate([1, 2, 3, 4])

    with pytest.raises(InvalidLengthError):
        test_instance.validate([])


def test_alternative_array_definition():
    test_instance = Array[String]

    assert test_instance.items == String
