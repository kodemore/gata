from typing import Any, Dict, ItemsView

from .dataclasses import (
    _dataclass_method_init,
    _dataclass_method_serialise,
    _dataclass_method_validate,
    _dataclass_method_deserialise,
    build_schema,
    _dataclass_method_frozen_getattr,
    _dataclass_method_frozen_setattr,
    _dataclass_method_repr,
    _dataclass_method_eq,
)
from .schema import Schema


class Dataclass:
    __frozen__: bool = False
    __validate__: bool = True
    __gata_schema__: Schema
    __frozen_dict__: Dict[str, Any]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.__frozen__ = kwargs.get("frozen", False)
        cls.__validate__ = kwargs.get("validate", True)
        cls.__gata_schema__ = build_schema(cls)
        cls.__class_name__ = cls.__qualname__

        if kwargs.get("repr", True):
            setattr(cls, "__repr__", _dataclass_method_repr)

        if kwargs.get("eq", True):
            setattr(cls, "__eq__", _dataclass_method_eq)

        if cls.__frozen__:
            setattr(cls, "__frozen_dict__", [])
            setattr(cls, "__setattr__", _dataclass_method_frozen_setattr)
            setattr(cls, "__getattr__", _dataclass_method_frozen_getattr)

    def __init__(self, *args, **kwargs):
        new_args = (self, *args)
        _dataclass_method_init(*new_args, **kwargs)

    def serialise(self, **mapping) -> Dict[str, Any]:
        return _dataclass_method_serialise(self, **mapping)

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        _dataclass_method_validate(cls, value=data)  # type: ignore

    @classmethod
    def deserialise(cls, value: Dict[str, Any]) -> "Dataclass":
        return _dataclass_method_deserialise(cls, value=value)

    def __iter__(self) -> ItemsView[str, Any]:  # type: ignore
        for key, value in self.serialise().items():
            yield key, value

    def __post_init__(self) -> None:
        ...
