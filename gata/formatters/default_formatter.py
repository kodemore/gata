from typing import Any

from gata.formatter import Formatter


class DefaultFormatter(Formatter):
    @classmethod
    def hydrate(cls, value: str) -> Any:
        return value

    @classmethod
    def extract(cls, value: Any) -> str:
        return value


__all__ = ["DefaultFormatter"]
