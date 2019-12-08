from typing import Any as TypingAny

from gata.errors import ValidationError
from .type import Type


class NullType(Type):
    def validate(self, value: TypingAny) -> None:
        if value is not None:
            raise ValidationError("Invalid value, expected None.")

    def __call__(
        self,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: TypingAny = None,
    ) -> None:
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")


Null = NullType()

__all__ = ["Null"]
