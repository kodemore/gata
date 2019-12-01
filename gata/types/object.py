from gata.errors import ValidationError
from gata.validators import validate
from .type import Type


class ObjectType(Type):
    def __init__(self):
        super().__init__()
        self.properties = {}
        self.required = []
        self._allow_overrides += (
            "properties",
            "required",
        )

    def __getitem__(self, key: str) -> Type:
        return self.properties[key]

    def __setitem__(self, key: str, value: Type):
        self.properties[key] = value

    def validate(self, value: dict) -> None:
        for prop in self.required:
            if prop not in value:
                raise ValidationError(
                    f"Missing required property `{prop}` in passed dataset `{value}`"
                )

        for key, prop in self.properties.items():
            if key not in value:
                continue
            prop.validate(value[key])

    def __call__(self, properties, **kwargs) -> "ObjectType":
        all_attributes = {**{"properties": properties}, **kwargs}
        return super().__call__(**all_attributes)


Object = ObjectType()


__all__ = ["Object"]
