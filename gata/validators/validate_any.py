from typing import Callable, Any, Sequence
from gata.errors.validation_error import ValidationError


def validate_any(value: Any, validators: Sequence[Callable]) -> bool:
    for validate in validators:
        try:
            validate(value)
            return True
        except ValueError:
            continue

    raise ValidationError(f"Could not validate value {value}, against set criteria.")


__all__ = ["validate_any"]
