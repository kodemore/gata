from typing import Any

from gata.errors import ValidationError


def validate_string(value: Any) -> bool:
    if not isinstance(value, str):
        raise ValidationError("Passed value is not a valid string value.")

    return True


__all__ = ["validate_string"]
