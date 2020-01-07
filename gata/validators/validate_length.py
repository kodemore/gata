from typing import Optional
from typing import Sized

from gata.errors import OverflowError
from gata.errors import UnderflowError


def validate_length(
    value: Sized, minimum: Optional[int] = None, maximum: Optional[int] = None
) -> bool:
    length = len(value)

    if minimum is not None and length < minimum:
        raise UnderflowError(
            f"Passed collection cannot be empty and must contain at least `{minimum}` items."
        )

    if maximum is not None and length > maximum:
        raise OverflowError(
            f"Passed collection cannot contain more than `{maximum}` items."
        )

    return True


__all__ = ["validate_length"]
