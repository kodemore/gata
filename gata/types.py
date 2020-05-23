from abc import ABC, abstractmethod
from typing import Any


class Type(ABC):
    @abstractmethod
    def validate(self) -> Any:
        ...

    @abstractmethod
    def serialise(self):
        ...
