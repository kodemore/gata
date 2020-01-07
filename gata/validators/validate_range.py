from typing import Optional
from typing import TypeVar
from gata.utils.comparable import Comparable
from gata.errors import NotWithinMaximumBoundaryError
from gata.errors import NotWithinMinimumBoundaryError


T = TypeVar("T", bound=Comparable)


def validate_range(
    value: T, minimum: Optional[T] = None, maximum: Optional[T] = None
) -> bool:
    if minimum is not None and value < minimum:
        raise NotWithinMinimumBoundaryError(
            f"Passed value `{value}` is lower than set minimum value `{minimum}`."
        )

    if maximum is not None and value > maximum:
        raise NotWithinMaximumBoundaryError(
            f"Passed value `{value}` is greater than set maximum value `{maximum}`."
        )

    return True


__all__ = ["validate_range"]
