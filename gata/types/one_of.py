from collections.abc import Iterable
from copy import deepcopy
from typing import Any as Any
from typing import List

from gata.errors import InvalidTypeError
from gata.errors import ValidationError
from .type import Type


class OneOfType(Type):
    def __init__(self):
        self.types = []

    def validate(self, value: Any) -> None:
        passed = 0
        for validator in self.types:
            try:
                validator.validate(value)
                passed += 1
            except ValidationError:
                continue

        if passed == 0:
            raise ValidationError(f"Could not validate value {value} against any rule.")

        if passed > 1:
            raise ValidationError(f"Passed value {value} conforms more than one rule")

    def __call__(
        self,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
    ) -> Type:
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")

    def __getitem__(self, types: List[Type]) -> "OneOfType":
        if not isinstance(types, Iterable):
            raise InvalidTypeError(
                f"gata.types.OneOf[] expects at least two types to be passed."
            )

        for item in types:
            if not isinstance(item, Type):
                raise InvalidTypeError(
                    f"Passed type {item} must be instance of gata.types.Type"
                )

        instance = deepcopy(self)
        instance.types = types
        return instance


OneOf = OneOfType()

__all__ = ["OneOf"]
