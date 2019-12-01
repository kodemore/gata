from typing import Optional
from typing import Union

from gata.errors import ValidationError
from gata.validators import validate_length
from .type import Type


class ArrayType(Type):
    def __init__(self):
        super().__init__()

        self.unique_items = False
        self.max_length = None
        self.min_length = None
        self._items = None

        self._allow_overrides += (
            "unique_items",
            "max_length",
            "min_length",
            "items",
        )

    @property
    def items(self) -> Optional[Type]:
        return self._items

    @items.setter
    def items(self, value: Type) -> None:
        """
        #todo: https://json-schema.org/understanding-json-schema/reference/array.html#tuple-validation tuple support
        :param Type value:
        :return:
        """
        if value and not isinstance(value, Type):
            raise ValueError(
                "items argument must be either None or instance of opyapi.schema.Type"
            )
        self._items = value

    def validate(self, value: Union[list, tuple]) -> None:

        if self.unique_items and not len(set(value)) == len(value):
            raise ValidationError(
                "Items in the array should be unique, passed array contains duplicates."
            )

        if self.items:
            for item in value:
                self._items.validate(item)

        if self.min_length or self.max_length:
            validate_length(value, self.min_length, self.max_length)

    def __getitem__(self, item):
        return self.__call__(item)

    def __call__(self, *args, **kwargs) -> "ArrayType":
        if args:
            kwargs["items"] = args[0]

        return super().__call__(**kwargs)


Array = ArrayType()

__all__ = ["Array"]
