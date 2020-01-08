from typing import Any
from typing import Callable, Sequence


def validate_all(value: Any, validators: Sequence[Callable[..., bool]]) -> bool:
    for validate in validators:
        validate(value)

    return True


__all__ = ["validate_all"]
