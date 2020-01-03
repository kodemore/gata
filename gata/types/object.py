from typing import Any

from gata.errors import ValidationError, FieldValidationError
from .string import String
from .type import Type


class Object(Type):
    def __init__(self, properties: dict, required: list = []):
        super().__init__()
        self.properties = properties
        self.required = required

    def validate(self, value: dict) -> None:
        for prop in self.required:
            if prop not in value:
                raise FieldValidationError(
                    prop,
                    ValidationError(
                        f"Missing required property `{prop}` in passed dataset `{value}`"
                    ),
                )

        for key, prop in self.properties.items():
            # Value is not within the object
            if key not in value:
                continue

            # Validate string
            if isinstance(prop, String.__class__) and not isinstance(value, str):
                try:
                    String.validate(value)
                except ValidationError as e:
                    raise FieldValidationError(key, e)

            # Validate property
            if isinstance(prop, Type):
                try:
                    prop.validate(value[key])
                except ValidationError as e:
                    raise FieldValidationError(key, e)

    def __call__(
        self,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
    ) -> Type:
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")


__all__ = ["Object"]
