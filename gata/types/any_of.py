from collections.abc import Iterable
from copy import deepcopy
from typing import Any as TypingAny
from typing import Tuple

from gata.errors import InvalidTypeError
from gata.errors import ValidationError
from .type import Type


class AnyOfType(Type):
    def __init__(self):
        self.types = []

    def validate(self, value: TypingAny) -> None:
        error = None
        for validator in self.types:
            try:
                validator.validate(value)
                break
            except ValidationError as e:
                error = e

        if error:
            raise error

    def __call__(self) -> None:
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")

    def __getitem__(self, types: Tuple[Type]) -> "AnyOfType":
        if not isinstance(types, Iterable):
            raise InvalidTypeError(
                f"gata.types.AnyOf[] expects at least two types to be passed."
            )

        for item in types:
            if not isinstance(item, Type):
                raise InvalidTypeError(
                    f"Passed type {item} must be instance of gata.types.Type"
                )

        instance = deepcopy(self)
        instance.types = types
        return instance


AnyOf = AnyOfType()

__all__ = ["AnyOf"]