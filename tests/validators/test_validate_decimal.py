from datetime import datetime

import pytest

from gata.errors import ValidationError
from gata.validators import validate_decimal
from decimal import Decimal


@pytest.mark.parametrize(
    "value", (Decimal("12.45"), "12.53", 12,),
)
def test_valid_values(value: str) -> None:
    assert isinstance(validate_decimal(value), Decimal)


@pytest.mark.parametrize("value", (None, "%%%"))
def test_invalid_values(value: str) -> None:
    with pytest.raises(ValidationError):
        validate_decimal(value)
