from typing import Any
from typing import Callable


def validate_nullable(value: Any, validator: Callable) -> bool:
    if value is None:
        return True
    return validator(value)


__all__ = ["validate_nullable"]
