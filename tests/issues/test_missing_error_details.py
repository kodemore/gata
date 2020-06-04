from dataclasses import dataclass as python_dataclass
from enum import Enum

from gata import dataclass, validate_dataclass
from gata.errors import FieldError


def test_missing_error_details_for_instantiation() -> None:
    class Status(Enum):
        PLACED = "placed"
        ACCEPTED = "accepted"
        CANCELLED = "cancelled"

    @dataclass
    class Order:
        description: str
        status: Status

    try:
        Order()
    except FieldError as error:
        assert error.context["field_name"] == "description"
        assert error.context["value"] is None
        assert error.context["expected_type"] is str
        assert error.code == "field_error"


def test_missing_error_details_for_validation() -> None:
    @python_dataclass
    class Order:
        description: str
        status: int

    try:
        order = Order(1, "a")
        validate_dataclass(order)
    except FieldError as error:
        assert error.context["field_name"] == "description"
        assert error.context["value"] == 1
        assert error.context["expected_type"] is str
        assert error.code == "field_error"
