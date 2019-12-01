from abc import ABC
from abc import abstractmethod
from copy import deepcopy
from typing import Any


class Type(ABC):
    """
    Reflects available types in the open api specification

    :: _Open Api types: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#data-types
    """

    def __init__(self):
        self.nullable = True
        self.default = None
        self.deprecated = False
        self.read_only = False
        self.write_only = False
        self._allow_overrides: tuple = (
            "deprecated",
            "write_only",
            "read_only",
            "nullable",
            "default",
        )

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass

    def __call__(self, **kwargs) -> "Type":
        """
        Overrides default creation of base classes, allowing for better type handling.
        :param kwargs:
        :return:
        """
        instance = deepcopy(self)
        for key, value in kwargs.items():
            if key not in self._allow_overrides:
                raise RuntimeError(
                    "Invalid attribute for type: "
                    + str(type(self))
                    + ", expected one of: "
                    + ",".join(map(str, self._allow_overrides))
                )
            setattr(instance, key, value)

        return instance


__all__ = ["Type"]
