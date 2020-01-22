from dataclasses import asdict, is_dataclass
from typing import Any

from .dataclass.deserialise import deserialise as generic_deserialise
from .dataclass.schema import get_dataclass_schema, validate
from .dataclass.serialise import serialise as generic_serialise
from .format import Format
from .validator import Validator


def serialise(value: Any) -> dict:
    dataclass_class = type(value)
    if not is_dataclass(dataclass_class):
        raise ValueError("Passed `value` must be instance of dataclass.")

    return generic_serialise(value, dataclass_class)


def deserialise(value: dict, target_class: Any) -> Any:
    if not is_dataclass(target_class):
        raise ValueError("Passed `target_class` must be valid dataclass.")

    return generic_deserialise(value, target_class)


def serialisable(cls_=None):
    def _attach_serialisable_interface(cls_):
        if not is_dataclass(cls_):
            raise AssertionError(
                "`serialisable()` decorator can be only used with dataclasses."
            )

        def _deserialise(value: dict):
            result = cls_.__new__(cls_)
            for key, type_ in cls_.__annotations__.items():
                if key not in value:
                    setattr(result, key, generic_deserialise(None, type_))
                    continue
                setattr(result, key, generic_deserialise(value[key], type_))

            return result

        def _serialise(*args):
            self = args[0]
            serialised = {}
            for key, type_ in cls_.__annotations__.items():
                serialised[key] = generic_serialise(getattr(self, key), type_)

            return serialised

        setattr(cls_, "serialise", _serialise)
        setattr(cls_, "deserialise", _deserialise)
        return cls_

    if cls_ is None:
        return _attach_serialisable_interface

    return _attach_serialisable_interface(cls_)


def validatable(cls_=None):
    def _attach_validatable_interface(cls_):
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
]
