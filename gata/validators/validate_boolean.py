from typing import Any

from gata.errors import ValidationError


def validate_boolean(value: Any) -> bool:
    if value is True or value is False:
        return True

    raise ValidationError("Passed value is not valid boolean value.")
