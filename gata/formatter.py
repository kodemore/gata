from abc import ABC
from abc import abstractmethod
from typing import Any


class Formatter(ABC):
    @classmethod
    @abstractmethod
    def hydrate(cls, value: str) -> Any:
        pass

    @classmethod
    @abstractmethod
    def extract(cls, value) -> str:
        pass
