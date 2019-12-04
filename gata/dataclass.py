from abc import ABCMeta
from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from gata.types.object import Object
from gata.types import map_type

T = TypeVar("T")


class DataClassMeta(ABCMeta):
    def __new__(mcs: Type[T], name: str, bases: tuple, namespace: dict, **kwargs) -> T:
        fqcn = f"{namespace['__module__']}.{namespace['__qualname__']}"
        klass: T = super().__new__(mcs, name, bases, namespace)  # type: ignore

        if fqcn == "gata.dataclass.DataClass":
            return klass

        properties = {}
        for attribute_name, attribute_type in klass.__annotations__.items():
            properties[attribute_name] = map_type(attribute_type)

        schema = Object(properties)

        def _validate(data: dict) -> None:
            schema.validate(data)

        def _create(data: dict):
            instance = klass.__new__(klass)
            for key, value in data.items():
                setattr(instance, key, value)

            return instance

        setattr(klass, "validate", _validate)
        setattr(klass, "create", _create)
        setattr(klass, "__schema__", schema)

        return klass


class DataClass(metaclass=DataClassMeta):
    __data__: Dict[str, Any]
    __schema__: Object

    def __getattr__(self, property_name):
        if property_name not in self.__schema__.properties:
            raise AttributeError(
                f"Property {property_name} is not defined in dataclass {self.__class__}"
            )

        return self.__data__[property_name] if property_name in self.__data__ else None

    def __setattr__(self, attribute_name: str, value: Any) -> None:
        pass


__all__ = ["DataClass"]
