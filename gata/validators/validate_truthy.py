from typing import Any

from gata.errors import ValidationError
from gata.types.formatters import BooleanFormatter


def validate_truthy(value: Any) -> None:
    try:
        formatted_value = BooleanFormatter.hydrate(value)
    except ValueError:
        raise ValidationError(f"Passed value {value} is not valid truthy expression.")

    if formatted_value is True:
        return

    raise ValidationError(f"Passed value {value} is not valid truthy expression.")


__all__ = ["validate_truthy"]
