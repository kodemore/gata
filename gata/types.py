from abc import ABC
from abc import abstractmethod
from typing import Any


class Type(ABC):
    @abstractmethod
    def validate(self) -> Any:
        ...

    @abstractmethod
    def serialise(self):
        ...
