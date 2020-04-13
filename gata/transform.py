from dataclasses import is_dataclass
from typing import Any, Callable, Dict, Type, TypeVar, Union

from .serialisable import Serialisable, serialise

T = TypeVar("T")


def transform(
    value: Union[Serialisable, Any],
    transform_to: Type[T],
    mapping: Dict[str, Union[str, bool, dict, Callable]],
) -> T:
    if not is_dataclass(transform_to):
        raise ValueError(
            "transform_to argument must be either dataclass or serialisable class"
        )
    if not is_dataclass(value):
        raise ValueError(
            "value argument must be either dataclass or serialisable instance"
        )

    all_fields = serialise(value, mapping) if mapping else serialise(value)
    allowed_fields = transform_to.__dataclass_fields__.keys()  # type: ignore

    fields = {}
    for field, value in all_fields.items():
        if field not in allowed_fields:
            continue
        fields[field] = value

    if hasattr(transform_to, "deserialise"):
        return transform_to.deserialise(fields)  # type: ignore

    instance = transform_to.__new__(transform_to)
    for name, value in fields.items():
        setattr(instance, name, value)

    return instance
