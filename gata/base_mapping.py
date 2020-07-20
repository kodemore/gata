from abc import ABC
from typing import Any, Optional, Union, Dict


class Mapping(ABC):
    def __init__(self, **kwargs):
        if not hasattr(self, "__annotations__"):
            return

        for property_name, property_type in self.__annotations__.items():
            if property_name in kwargs:
                setattr(self, property_name, kwargs[property_name])
                continue
            setattr(self, property_name, None)

    def validate(self, value: Any) -> Any:
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value

    def deserialise(self, value: Any) -> Any:
        return value
