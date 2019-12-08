from typing import Any

from gata.errors import ValidationError
from .type import Type
from .string import String


class Object(Type):
    def __init__(self, properties: dict, required: list = []):
        super().__init__()
        self.properties = properties
        self.required = required

    def validate(self, value: dict) -> None:
        for prop in self.required:
            if prop not in value:
                raise ValidationError(
                    f"Missing required property `{prop}` in passed dataset `{value}`"
                )

        for key, prop in self.properties.items():
            # Value is not within the object
            if key not in value:
                continue
            # Value has been already formatted, thus it is valid
            if isinstance(prop, String.__class__) and not isinstance(value, str):
                continue
            # Validate property
            if isinstance(prop, Type):
                prop.validate(value[key])

    def __call__(
        self,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
    ) -> None:
        raise RuntimeError(f"Cannot recreate instance of {self.__class__}.")


__all__ = ["Object"]
