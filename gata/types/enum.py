from typing import Any
from typing import List

from gata.errors import ValidationError
from .type import Type


class Enum(Type):
    def __init__(self, *args):
        super().__init__()
        self.values = args

    def validate(self, value: Any) -> None:
        if value not in self.values:
            raise ValidationError(
                f"Passed value `{value}` is not within allowed values `{self.values}`."
            )

    def __call__(
            self,
            deprecated: bool = False,
            write_only: bool = False,
            read_only: bool = False,
            nullable: bool = False,
            default: Any = None,
    ) -> "Enum":
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")


__all__ = ["Enum"]
