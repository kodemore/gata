from datetime import date
from typing import Optional

from gata.errors import NotWithinMaximumBoundaryError
from gata.errors import NotWithinMinimumBoundaryError
from gata.errors import ValidationError
from gata.formatters import DateFormatter


def validate_date(
    value: str, minimum: Optional[date] = None, maximum: Optional[date] = None
) -> bool:
    try:
        date_value = DateFormatter.hydrate(value)
    except ValueError:
        raise ValidationError(f"Passed value {value} is not valid ISO 8601 date.")

    if not date_value:
        raise ValidationError(f"Passed value {value} is not valid ISO 8601 date.")

    if minimum and date_value < minimum:
        raise NotWithinMinimumBoundaryError(
            f"Passed date `{date_value}` is lower than set minimum value `{minimum}`."
        )

    if maximum and date_value > maximum:
        raise NotWithinMaximumBoundaryError(
            f"Passed date `{date_value}` is greater than set maximum value `{maximum}`."
        )

    return True


__all__ = ["validate_date"]
