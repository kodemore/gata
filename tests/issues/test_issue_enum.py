from enum import Enum
import pytest
from gata import dataclass


def test_issue_enum() -> None:
    class Status(Enum):
        PLACED = "placed"
        ACCEPTED = "accepted"
        CANCELLED = "cancelled"

    @dataclass
    class Order:
        description: str
        status: Status

    instance = Order(**{"description": "Test order", "status": "placed"})
    assert isinstance(instance, Order)

    with pytest.raises(ValueError):
        Order(**{"description": "Test order", "status": "unknown"})

    assert dict(instance) == {
        "description": "Test order",
        "status": "placed",
    }
