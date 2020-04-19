from dataclasses import dataclass as base_dataclass, field, is_dataclass
from typing import Any, Callable, Dict, Generator, TypeVar, Union

from typing_extensions import Protocol, runtime_checkable

from .deserialise import deserialise as deserialise_type, deserialise_dataclass
from .schema import UNDEFINED, get_dataclass_schema
from .serialise import serialise_dataclass

T = TypeVar("T")


@runtime_checkable
class Validatable(Protocol):
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        ...


@runtime_checkable
class Serialisable(Protocol):
    @classmethod
    def deserialise(cls, data: Dict[str, Any]) -> T:
        ...

    def serialise(self, **mapping) -> Dict[str, Any]:
        ...


def serialise(value: Any, mapping: Dict[str, Union[str, bool, dict, Callable]] = None) -> dict:
    dataclass_class = type(value)
    if not is_dataclass(dataclass_class):
        raise ValueError("Passed `value` must be instance of dataclass.")

    return serialise_dataclass(value, dataclass_class, mapping)


def deserialise(value: dict, target_class: Any) -> Any:
    if not is_dataclass(target_class):
        raise ValueError("Passed `target_class` must be valid dataclass.")

    return deserialise_dataclass(value, target_class)


def dataclass(
    _cls: T = None, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False
) -> Union[T, Validatable, Serialisable, Callable[[T], Union[T, Validatable, Serialisable]]]:
    def _make_dataclass(_cls: T) -> Union[T, Validatable, Serialisable]:
        _cls = base_dataclass(  # type: ignore
            _cls, init=False, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen
        )
        schema = get_dataclass_schema(_cls)

        def _serialise(*args, **mapping) -> Dict[str, Any]:
            self = args[0]
            return serialise_dataclass(self, _cls, mapping)

        def _as_dict(*args) -> Generator:
            self = args[0]
            for key, value in serialise_dataclass(self, _cls).items():
                yield key, value

        setattr(_cls, "validate", lambda value: schema.validate(value))
        setattr(_cls, "serialise", _serialise)
        setattr(_cls, "__iter__", _as_dict)
        if not init:
            return _cls

        old_init = getattr(_cls, "__init__")

        def _init(*args, **kwargs) -> None:
            self = args[0]
            if old_init != object.__init__:
                old_init(*args, **kwargs)
                _cls.validate(self.serialise())
                return None

            schema.validate(kwargs)
            for key, schema_field in schema:
                if schema_field.read_only:
                    continue

                if key not in kwargs:
                    default_value = schema_field.default
                    if default_value is UNDEFINED:
                        continue
                    setattr(self, key, default_value)
                    continue

                value = kwargs[key]
                if schema_field.deserialiser:
                    setattr(self, key, schema_field.deserialiser(value, schema_field.type))
                    continue

                setattr(self, key, deserialise_type(value, schema_field.type))

            if hasattr(self, '__post_init__'):
                self.__post_init__()

        setattr(_cls, "__init__", _init)

        return _cls

    if _cls is None:
        return _make_dataclass

    return _make_dataclass(_cls)


__all__ = ["serialise", "deserialise", "dataclass", "Serialisable", "Validatable", "field"]
