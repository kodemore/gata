from typing import Any as NativeAny
from typing import Optional
from typing import Union

from gata.errors import ValidationError
from gata.validators import validate_length
from .any import Any
from .type import Type


class ArrayType(Type):
    def __init__(self):
        super().__init__()

        self.unique_items = False
        self.max_length = None
        self.min_length = None
        self.items = None

    def validate(self, value: Union[list, tuple]) -> None:

        if self.unique_items and not len(set(value)) == len(value):
            raise ValidationError(
                "Items in the array should be unique, passed array contains duplicates."
            )

        if self.items:
            for item in value:
                self.items.validate(item)

        if self.min_length or self.max_length:
            validate_length(value, self.min_length, self.max_length)

    def __getitem__(self, items: Type) -> "ArrayType":
        return self.__call__(items=items)

    def __call__(
        self,
        items: Type = Any,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        unique_items: bool = False,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: NativeAny = None,
    ) -> "ArrayType":
        instance: ArrayType = super().__call__(
            deprecated, write_only, read_only, nullable, default
        )
        instance.items = items
        instance.max_length = max_length
        instance.min_length = min_length
        instance.unique_items = unique_items

        return instance


Array = ArrayType()

__all__ = ["Array"]
