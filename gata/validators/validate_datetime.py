from datetime import datetime
from typing import Optional

from gata.errors import NotWithinMaximumBoundaryError
from gata.errors import NotWithinMinimumBoundaryError
from gata.errors import ValidationError
from gata.types.formatters import DateTimeFormatter


def validate_datetime(
    value: str, minimum: Optional[datetime] = None, maximum: Optional[datetime] = None
) -> None:
    try:
        datetime_value = DateTimeFormatter.hydrate(value)
    except ValueError:
        raise ValidationError(f"Passed value {value} is not valid ISO 8601 datetime")

    if minimum and datetime_value < minimum:
        raise NotWithinMinimumBoundaryError(
            f"Passed date `{datetime_value}` is lower than set minimum value `{minimum}`."
        )

    if maximum and datetime_value > maximum:
        raise NotWithinMaximumBoundaryError(
            f"Passed date `{datetime_value}` is greater than set maximum value `{maximum}`."
        )


__all__ = ["validate_datetime"]
