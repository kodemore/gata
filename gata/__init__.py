from dataclasses import asdict, is_dataclass
from functools import partial
from typing import Any, Callable, Dict, TypeVar, Union

from typing_extensions import Protocol

from .dataclass.deserialise import deserialise_dataclass
from .dataclass.schema import MetaProperty, get_dataclass_schema, validate
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


def serialise(value: Any) -> dict:
    dataclass_class = type(value)
    if not is_dataclass(dataclass_class):
        raise ValueError("Passed `value` must be instance of dataclass.")

    return serialise_dataclass(value, dataclass_class)


def deserialise(value: dict, target_class: Any) -> Any:
    if not is_dataclass(target_class):
        raise ValueError("Passed `target_class` must be valid dataclass.")

    return deserialise_dataclass(value, target_class)


def serialisable(
    cls_: T = None,
) -> Union[T, Serialisable, Callable[[Any], Union[T, Serialisable]]]:
    def _attach_serialisable_interface(cls_) -> Union[T, Serialisable]:
        if not is_dataclass(cls_):
            raise AssertionError(
                "`serialisable()` decorator can be only used with dataclasses."
            )

        def _serialise(*args):
            self = args[0]
            return serialise_dataclass(self, cls_)

        setattr(cls_, "serialise", _serialise)
        setattr(cls_, "deserialise", partial(deserialise_dataclass, source_type=cls_))
        return cls_

    if cls_ is None:
        return _attach_serialisable_interface

    return _attach_serialisable_interface(cls_)


def validatable(
    cls_: T = None,
) -> Union[T, Validatable, Callable[[Any], Union[T, Validatable]]]:
    def _attach_validatable_interface(cls_) -> Union[T, Validatable]:
        if not is_dataclass(cls_):
            raise AssertionError(
                "`validatable()` decorator can be only used with dataclasses."
            )
        schema = get_dataclass_schema(cls_)
        old_init = getattr(cls_, "__init__")

        def _init(*args, **kwargs):
            self = args[0]
            old_init(*args, **kwargs)
            schema.validate(asdict(self))

        setattr(cls_, "__init__", _init)
        setattr(cls_, "validate", lambda value: schema.validate(value))

        return cls_

    if cls_ is None:
        return _attach_validatable_interface

    return _attach_validatable_interface(cls_)


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
    "MetaProperty",
]
