from typing import Any

from gata.errors import ValidationError
from gata.formatters import BooleanFormatter


def validate_truthy(value: Any) -> bool:
    try:
        formatted_value = BooleanFormatter.hydrate(value)
    except ValueError:
        raise ValidationError(f"Passed value {value} is not valid truthy expression.")

    if formatted_value is True:
        return True

    raise ValidationError(f"Passed value {value} is not valid truthy expression.")


__all__ = ["validate_truthy"]
