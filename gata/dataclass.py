from abc import ABCMeta
from typing import Any
from typing import Dict
from typing import TypeVar

from gata.types.object import Object
from gata.types.type import Type

T = TypeVar("T")


class DataClassMeta(ABCMeta):
    pass


class DataClass(metaclass=DataClassMeta):
    __data__: Dict[str, Any]
    __schema__: Object

    def __init__(self, **kwargs) -> None:
        pass

    def __getattr__(self, attribute_name):
        pass

    def __setattr__(self, attribute_name: str, value: Any) -> None:
        pass


__all__ = ["DataClass"]
