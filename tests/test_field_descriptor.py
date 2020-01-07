from gata.field_descriptor import FieldDescriptor
from gata.errors import InvalidLengthError
from typing import List
import pytest


def test_can_instantiate_field_descriptor() -> None:
    field = FieldDescriptor(str, {"format": "email"})
    assert isinstance(field, FieldDescriptor)


def test_validate_field_descriptor_for_formatted_string() -> None:
    field = FieldDescriptor(str, {"format": "email"})

    assert field.validate("test@email.com")

    with pytest.raises(ValueError):
        field.validate("test")


def test_validate_field_descriptor_for_formatter_list_of_strings() -> None:
    field = FieldDescriptor(
        List[str], {"min": 1, "max": 3, "items": {"format": "email"}}
    )

    assert field.validate(["test@email.com", "test_2@email.com"])

    with pytest.raises(InvalidLengthError):
        field.validate([])

    with pytest.raises(ValueError):
        field.validate(["a"])

    with pytest.raises(InvalidLengthError):
        field.validate(
            ["test@email.com", "test@email.com", "test@email.com", "test@email.com"]
        )


def test_validate_field_descriptor_min_max_length_for_string() -> None:
    field = FieldDescriptor(str, {"min": 1, "max": 3})

    assert field.validate("a")
    assert field.validate("aa")
    assert field.validate("aaa")

    with pytest.raises(InvalidLengthError):
        field.validate("")

    with pytest.raises(InvalidLengthError):
        field.validate("1234")
