from copy import deepcopy
from typing import Any
from typing import List
from typing import Union

from gata.errors import ValidationError
from .type import Type


class EnumType(Type):
    def __init__(self):
        super().__init__()
        self.values = []
        self.target = None

    def validate(self, value: Any) -> None:
        if value not in self.values:
            if self.target and isinstance(value, self.target):
                return None
            raise ValidationError(
                f"Passed value `{value}` is not within allowed values `{self.values}`."
            )

    def __call__(
        self,
        values: List[Union[str, int]],
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
    ) -> "EnumType":
        instance: EnumType = super().__call__(
            deprecated, write_only, read_only, nullable, default
        )
        instance.values = values

        return instance

    def __getitem__(self, values: List[Union[str, int]]) -> "EnumType":

        instance = deepcopy(self)
        instance.values = set(values)
        return instance


Enum = EnumType()

__all__ = ["Enum"]
