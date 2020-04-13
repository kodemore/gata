from dataclasses import is_dataclass
from functools import partial
from typing import Any, Callable, Dict, TypeVar, Union

from typing_extensions import Protocol

from .dataclass.deserialise import deserialise_dataclass
from .dataclass.serialise import serialise_dataclass
from .utils import convert_to_dataclass

T = TypeVar("T")


class Serialisable(Protocol):
    @classmethod
    def deserialise(cls, data: Dict[str, Any]) -> T:
        ...

    def serialise(self, **mapping) -> Dict[str, Any]:
        ...


def serialise(
    value: Any, mapping: Dict[str, Union[str, bool, dict, Callable]] = None
) -> dict:
    dataclass_class = type(value)
    if not is_dataclass(dataclass_class):
        raise ValueError("Passed `value` must be instance of dataclass.")

    return serialise_dataclass(value, dataclass_class, mapping)


def deserialise(value: dict, target_class: Any) -> Any:
    if not is_dataclass(target_class):
        raise ValueError("Passed `target_class` must be valid dataclass.")

    return deserialise_dataclass(value, target_class)


def serialisable(
    _cls: T = None,
) -> Union[T, Serialisable, Callable[[Any], Union[T, Serialisable]]]:
    def _attach_serialisable_interface(_cls) -> Union[T, Serialisable]:
        if not is_dataclass(_cls):
            _cls = convert_to_dataclass(_cls)

        def _serialise(*args, **mapping):
            self = args[0]
            return serialise_dataclass(self, _cls, mapping)

        setattr(_cls, "serialise", _serialise)
        setattr(_cls, "deserialise", partial(deserialise_dataclass, source_type=_cls))
        return _cls

    if _cls is None:
        return _attach_serialisable_interface

    return _attach_serialisable_interface(_cls)


__all__ = ["serialise", "deserialise", "serialisable", "Serialisable"]
