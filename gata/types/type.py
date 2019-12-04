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
        self.nullable = False
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

    def __call__(
        self,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
    ) -> "Type":
        """
        Overrides default creation of base classes, allowing for better type handling.
        """
        instance = deepcopy(self)
        instance.deprecated = deprecated
        instance.write_only = write_only
        instance.read_only = read_only
        instance.nullable = nullable
        instance.default = default

        return instance


__all__ = ["Type"]
