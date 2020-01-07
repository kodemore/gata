from typing import Any

from gata.errors import ValidationError


def validate_integer(value: Any) -> bool:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError("Passed value is not a valid integer number.")

    return True


__all__ = ["validate_integer"]
