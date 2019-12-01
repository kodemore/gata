from typing import Any

from gata.errors import ValidationError
from gata.types.formatters import BooleanFormatter


def validate_falsy(value: Any) -> None:
    try:
        formatted_value = BooleanFormatter.hydrate(value)
    except ValueError:
        raise ValidationError(f"Passed value {value} is not valid falsy expression.")

    if formatted_value is False:
        return

    raise ValidationError(f"Passed value {value} is not valid falsy expression.")


__all__ = ["validate_falsy"]
