from gata.errors import ValidationError
from numbers import Complex
from typing import Union


def validate_multiple_of(
    value: Union[float, int, Complex], multiple_of: Union[float, int, Complex]
) -> bool:
    if not value % multiple_of == 0:
        raise ValidationError(
            f"Passed value `{value}` must be multiplication of {multiple_of}."
        )

    return True


__all__ = ["validate_multiple_of"]
