from typing import Optional

from gata.errors import NotWithinMaximumBoundaryError
from gata.errors import NotWithinMinimumBoundaryError


def validate_range(
    value: float, minimum: Optional[float] = None, maximum: Optional[float] = None
):
    if minimum is not None and value < minimum:
        raise NotWithinMinimumBoundaryError(
            f"Passed value `{value}` is lower than set minimum value `{minimum}`."
        )

    if maximum is not None and value > maximum:
        raise NotWithinMaximumBoundaryError(
            f"Passed value `{value}` is greater than set maximum value `{maximum}`."
        )


__all__ = ["validate_range"]
