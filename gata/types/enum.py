from typing import Any
from typing import List

from gata.errors import ValidationError
from .type import Type


class EnumType(Type):
    def __init__(self):
        super().__init__()
        self._allow_overrides += (
            "enum",
        )
        self.enum = []

    def validate(self, value: Any) -> None:
        if value not in self.enum:
            raise ValidationError(
                f"Passed value `{value}` is not within allowed values `{self.enum}`."
            )

        return value

    def __call__(self, *args: List[str], **kwargs):
        kwargs["enum"] = args
        return super().__call__(**kwargs)


Enum = EnumType()

__all__ = ["Enum"]
