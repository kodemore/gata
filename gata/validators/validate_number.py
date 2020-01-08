import numbers
from typing import Optional
from typing import Union

from gata.errors import NotWithinMaximumBoundaryError
from gata.errors import NotWithinMinimumBoundaryError
from gata.errors import ValidationError
from .validate_multiple_of import validate_multiple_of


def validate_number(
    value: Union[int, float],
    minimum: Optional[Union[int, float]] = None,
    maximum: Optional[Union[int, float]] = None,
    multiple_of: Optional[Union[int, float]] = None,
) -> bool:
    if isinstance(value, bool) or not isinstance(
        value, (int, float, complex, numbers.Real, numbers.Rational)
    ):
        raise ValidationError("Passed value is not a valid number.")

    if minimum and value < minimum:
        raise NotWithinMinimumBoundaryError(
            f"Passed value `{value}` is lower than set minimum value `{minimum}`."
        )

    if maximum and value > maximum:
        raise NotWithinMaximumBoundaryError(
            f"Passed value `{value}` is greater than set maximum value `{maximum}`."
        )

    if multiple_of:
        validate_multiple_of(value, multiple_of)  # type: ignore

    return True


__all__ = ["validate_number"]
