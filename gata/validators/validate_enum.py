from enum import Enum
from typing import Any
from typing import Type

from gata.errors import ValidationError


def validate_enum(value: Any, enum: Type[Enum]) -> bool:
    try:
        enum(value)
    except ValueError:
        raise ValidationError(f"Passed value is not valid value for {enum.__class__}.")

    return True


__all__ = ["validate_enum"]
