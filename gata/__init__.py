from dataclasses import asdict, is_dataclass, dataclass as base_dataclass
from functools import partial
from typing import Any, Callable, Dict, TypeVar, Union, Type

from typing_extensions import Protocol

from .dataclass.deserialise import deserialise_dataclass
from .dataclass.schema import PropertyMeta, get_dataclass_schema, validate
from .dataclass.serialise import serialise_dataclass
from .format import Format
from .validator import Validator

T = TypeVar("T")


class Validatable(Protocol):
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        ...


class Serialisable(Protocol):
    @classmethod
    def deserialise(cls, data: Dict[str, Any]) -> T:
        ...

    def serialise(self) -> Dict[str, Any]:
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


def _convert_to_dataclass(cls: Type[T]) -> Type[T]:
    return base_dataclass(cls, init=False, repr=False, eq=False)  # type: ignore


def serialisable(
    _cls: T = None,
) -> Union[T, Serialisable, Callable[[Any], Union[T, Serialisable]]]:
    def _attach_serialisable_interface(_cls) -> Union[T, Serialisable]:
        if not is_dataclass(_cls):
            _cls = _convert_to_dataclass(_cls)

        def _serialise(*args, **mapping):
            self = args[0]
            return serialise_dataclass(self, _cls, mapping)

        setattr(_cls, "serialise", _serialise)
        setattr(_cls, "deserialise", partial(deserialise_dataclass, source_type=_cls))
        return _cls

    if _cls is None:
        return _attach_serialisable_interface

    return _attach_serialisable_interface(_cls)


def validatable(
    _cls: T = None,
) -> Union[T, Validatable, Callable[[Any], Union[T, Validatable]]]:
    def _attach_validatable_interface(_cls) -> Union[T, Validatable]:
        if not is_dataclass(_cls):
            _cls = _convert_to_dataclass(_cls)

        schema = get_dataclass_schema(_cls)
        old_init = getattr(_cls, "__init__")

        def _init(*args, **kwargs):
            self = args[0]
            old_init(*args, **kwargs)
            schema.validate(asdict(self))

        setattr(_cls, "__init__", _init)
        setattr(_cls, "validate", lambda value: schema.validate(value))

        return _cls

    if _cls is None:
        return _attach_validatable_interface

    return _attach_validatable_interface(_cls)


__all__ = [
    "serialisable",
    "validatable",
    "serialise",
    "deserialise",
    "validate",
    "Format",
    "Validator",
    "Serialisable",
    "Validatable",
    "PropertyMeta",
]
