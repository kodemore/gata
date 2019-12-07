from typing import Any as TypingAny

from .type import Type


class AnyType(Type):
    def validate(self, value: TypingAny) -> None:
        pass

    def __call__(
            self,
            deprecated: bool = False,
            write_only: bool = False,
            read_only: bool = False,
            nullable: bool = False,
            default: TypingAny = None,
    ) -> None:
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")


Any = AnyType()

__all__ = ["Any"]
