from abc import ABCMeta
from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from .errors.field_error import FieldError
from .field_descriptor import FieldDescriptor
from .unserialise import unserialise
from .serialise import serialise

T = TypeVar("T")


class DataClassMeta(ABCMeta):
    def __new__(mcs: Type[T], name: str, bases: tuple, namespace: dict, **kwargs) -> T:
        fqcn = f"{namespace['__module__']}.{namespace['__qualname__']}"
        klass: T = super().__new__(mcs, name, bases, namespace)  # type: ignore

        if fqcn == "gata.dataclass.DataClass":
            return klass

        meta = None
        if hasattr(klass, "Meta"):
            meta = getattr(klass, "Meta")

        dataclass = {}
        for attribute_name, attribute_type in klass.__annotations__.items():
            field_meta = getattr(meta, attribute_name, {}) if meta else {}
            dataclass[attribute_name] = FieldDescriptor(attribute_type, field_meta)

        def _validate(data: dict) -> bool:
            # Check for unknown fields
            for key, value in data.items():
                if key not in dataclass:
                    raise ValueError(
                        f"Attribute `{key}` is not defined in dataclass {klass}"
                    )
            for field_name, field_descriptor in dataclass.items():
                try:
                    value = data.get(
                        field_name,
                        getattr(klass, field_name)
                        if hasattr(klass, field_name)
                        else None,
                    )
                    field_descriptor.validate(value)
                except ValueError as error:
                    raise FieldError(field_name, error)

            return True

        def _unserialise(data: dict):
            instance = klass.__new__(klass)  # type: ignore

            for key, value in data.items():
                if key not in dataclass:
                    raise AttributeError(
                        f"Attribute `{key}` is not defined in dataclass {klass}"
                    )
                field = dataclass[key]

                try:
                    unserialised_value = unserialise(value, field.type, field.meta)
                    # Lets validate raw values
                    if isinstance(unserialised_value, str):
                        field.validate(unserialised_value)

                    instance.__dict__[key] = unserialised_value
                except ValueError as error:
                    raise FieldError(key, error)

            return instance

        setattr(klass, "validate", _validate)
        setattr(klass, "unserialise", _unserialise)
        setattr(klass, "__dataclass__", dataclass)

        return klass


class DataClass(metaclass=DataClassMeta):
    __dataclass__: Dict

    def __getattr__(self, attribute):
        if not self.__hasattr__(attribute):
            raise AttributeError(
                f"Attribute `{attribute}` is not defined in dataclass {self.__class__}"
            )

        return self.__dict__[attribute] if attribute in self.__dict__ else None

    def __setattr__(self, attribute: str, value: Any) -> None:
        if not self.__hasattr__(attribute):
            raise AttributeError(
                f"Property {attribute} is not defined in dataclass {self.__class__}"
            )
        field_descriptor = self.__dataclass__[attribute]
        field_descriptor.validate(value)
        self.__dict__[attribute] = value

    def __hasattr__(self, attribute_name: str) -> bool:
        return attribute_name in self.__dataclass__

    def serialise(self) -> dict:
        serialised = {}
        for field_name, field_descriptor in self.__dataclass__.items():
            serialised[field_name] = serialise(
                getattr(self, field_name), field_descriptor.type
            )

        return serialised

    @classmethod
    def unserialise(cls, properties: dict) -> "DataClass":
        raise NotImplemented()

    @classmethod
    def validate(cls, properties: dict) -> bool:
        raise NotImplemented()


__all__ = ["DataClass"]
