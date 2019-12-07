from abc import ABCMeta
from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from gata.types.object import Object
from gata.types.utils import map_type

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

    def __getattr__(self, attribute):
        if not self.__hasattr__(attribute):
            raise AttributeError(
                f"Attribute `{attribute}` is not defined in dataclass {self.__class__}"
            )

        return self.__dict__[attribute] if attribute in self.__dict__["__data__"] else None

    def __setattr__(self, attribute: str, value: Any) -> None:
        if not self.__hasattr__(attribute):
            raise AttributeError(
                f"Property {attribute} is not defined in dataclass {self.__class__}"
            )
        self.__dict__[attribute] = value
        self.__schema__.validate(self.__dict__)

    def __hasattr__(self, attribute_name: str) -> bool:
        return attribute_name in self.__schema__.properties

    def as_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def create(cls, properties: dict) -> "DataClass":
        pass

    @classmethod
    def validate(cls, properties: dict) -> None:
        pass


__all__ = ["DataClass"]
