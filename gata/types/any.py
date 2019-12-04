from typing import Any

from .type import Type


class AnyType(Type):
    def validate(self, value: Any) -> None:
        pass

    def __call__(
            self,
            deprecated: bool = False,
            write_only: bool = False,
            read_only: bool = False,
            nullable: bool = False,
            default: Any = None,
    ) -> None:
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")


Any = AnyType()

__all__ = ["Any"]
