from typing import Any

from gata.errors import ValidationError
from .type import Type


class BooleanType(Type):
    def validate(self, value: Any) -> None:
        if value is True or value is False:
            return None

        raise ValidationError("Passed value is not valid boolean value.")

    def __call__(
        self,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
    ) -> "BooleanType":
        instance: BooleanType = super().__call__(deprecated, write_only, read_only, nullable, default)  # type: ignore

        return instance


Boolean = BooleanType()

__all__ = ["Boolean"]
