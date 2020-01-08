from typing import Callable
from typing import Iterable
from typing import Sized

from gata.errors import ValidationError


def validate_array(value: Sized, items: Callable = None, unique: bool = False) -> bool:
    if not isinstance(value, Iterable) or isinstance(value, str):
        raise ValidationError("Passed value is not a valid array type.")

    if isinstance(value, Sized) and unique and not len(set(value)) == len(value):
        raise ValidationError(
            "Items in the array should be unique, passed array contains duplicates."
        )

    if items:
        for item in value:
            items(item)

    return True


__all__ = ["validate_array"]
