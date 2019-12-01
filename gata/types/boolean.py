from typing import Any

from .type import Type


class BooleanType(Type):
    def validate(self, value: Any) -> None:
        pass


Boolean = BooleanType()

__all__ = ["Boolean"]
