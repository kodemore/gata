from abc import ABCMeta
from enum import Enum
from inspect import isclass
from typing import Any
from typing import Type
from typing import TypeVar
from typing import Union

from gata.errors import FieldValidationError
from gata.types import Type as GataType
from gata.types.array import Array
from gata.types.enum import Enum as GataEnum
from gata.types.object import Object
from gata.types.string import String
from gata.types.utils.map_type import map_type

T = TypeVar("T")


def unserialise_value(schema: GataType, value: Any) -> Any:
    # Formatted strings
    if isinstance(schema, String.__class__):
        if schema.format:
            return schema.format.value.hydrate(value)
        return value

    # Enums
    if isinstance(schema, GataEnum.__class__) and schema.target:
        return schema.target(value)

    # Dataclasses
    if isclass(schema) and issubclass(schema, DataClass):  # type: ignore
        return schema.create(value)  # type: ignore

    # Lists and sets
    if isinstance(schema, Array.__class__) and schema.items:
        items = []
        for item in value:
            items.append(unserialise_value(schema.items, item))
        if schema.unique_items:
            return set(items)

        return items

    # Ignore
    return value


def serialise_value(schema: GataType, value: Any) -> Any:
    # Formatted strings
    if isinstance(schema, String.__class__):
        if schema.format:
            return schema.format.value.extract(value)
        return value

    # Enums
    if isinstance(schema, GataEnum.__class__):
        if isinstance(value, Enum):
            return value.value
        return value

    # Dataclasses
    if isclass(schema) and issubclass(schema, DataClass):  # type: ignore
        return schema.serialise(value)  # type: ignore

    # Lists and sets
    if isinstance(schema, Array.__class__) and schema.items:
        items = []
        for item in value:
            items.append(serialise_value(schema.items, item))
        return items

    return value


class DataClassMeta(ABCMeta):
    def __new__(mcs: Type[T], name: str, bases: tuple, namespace: dict, **kwargs) -> T:
        fqcn = f"{namespace['__module__']}.{namespace['__qualname__']}"
        klass: T = super().__new__(mcs, name, bases, namespace)  # type: ignore

        if fqcn == "gata.dataclass.DataClass":
            return klass

        properties = {}
        for attribute_name, attribute_type in klass.__annotations__.items():
            properties[attribute_name] = map_type(attribute_type)

        dataclass = Object(properties)

        def _validate(data: Union[DataClass, dict]) -> None:
            if isinstance(
                data, DataClass
            ):  # Do not validate dataclasses, this can cause infinite recursion.
                return None

            dataclass.validate(data)

        def _create(data: dict):
            instance = klass.__new__(klass)  # type: ignore

            for key, value in data.items():
                if key not in dataclass.properties:
                    raise AttributeError(
                        f"Attribute `{key}` is not defined in dataclass {klass}"
                    )

                try:
                    dataclass.properties[key].validate(value)
                except ValueError as error:
                    raise FieldValidationError(key, error)

                try:
                    instance.__dict__[key] = unserialise_value(
                        dataclass.properties[key], value
                    )
                except ValueError as error:
                    raise FieldValidationError(key, error)

            return instance

        setattr(klass, "validate", _validate)
        setattr(klass, "create", _create)
        setattr(klass, "__dataclass__", dataclass)

        return klass


class DataClass(metaclass=DataClassMeta):
    __dataclass__: Object

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
        self.__dict__[attribute] = value
        self.__dataclass__.validate(self.__dict__)

    def __hasattr__(self, attribute_name: str) -> bool:
        return attribute_name in self.__dataclass__.properties

    def serialise(self) -> dict:
        serialised = {}
        for key, value in self.__dataclass__.properties.items():
            serialised[key] = serialise_value(value, getattr(self, key))
        return serialised

    @classmethod
    def create(cls, properties: dict) -> "DataClass":
        raise NotImplemented()

    @classmethod
    def validate(cls, properties: dict) -> None:
        raise NotImplemented()


__all__ = ["DataClass", "unserialise_value", "serialise_value"]
