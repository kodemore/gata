import numbers
from typing import Any

from gata.errors import ValidationError


def validate_number(value: Any) -> bool:
    if isinstance(value, bool) or not isinstance(
        value, (int, float, complex, numbers.Number, numbers.Real, numbers.Rational)
    ):
        raise ValidationError("Passed value is not a valid number.")

    return True


__all__ = ["validate_number"]
