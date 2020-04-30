import dataclasses
from collections import OrderedDict
from decimal import Decimal
from typing import Any, Callable, Dict, Iterable, Type, Union

from gata.format import Format
from gata.inspect import is_dataclass_like
from gata.typing import ConstrainedInteger, SerialisableType, ValidatableType, ConstrainedBoolean, ConstrainedFloat, ConstrainedString

_TYPE_MAPPING = {
    bool: ConstrainedBoolean,
    int: ConstrainedInteger,
    float: ConstrainedFloat,
    str: ConstrainedString,
}


def build_schema(_cls: Any) -> "Schema":
    if not is_dataclass_like(_cls):
        raise ValueError(f"passed value {_cls} is not valid dataclass type")

    schema = Schema(_cls)
    for field_name, field_type in _cls.__annotations__.items():
        field_definition = Field()

        if hasattr(_cls, field_name):
            field_value = getattr(_cls, field_name)
            if isinstance(field_value, dataclasses.Field):
                field_definition.compare = field_value.compare
                field_definition.repr = field_value.repr
                field_definition._default = field_value.default
                field_definition._default_factory = field_value.default_factory  # type: ignore
            elif isinstance(field_value, Field):
                field_definition = field_value
            else:
                field_definition._default = field_value

        field_definition._type = field_type
        if field_type in _TYPE_MAPPING:
            schema_type = _TYPE_MAPPING[field_type]
        else:
            schema_type = field_type

        if not field_definition._serialiser and issubclass(schema_type, SerialisableType):
            field_definition._serialiser = lambda value: schema_type.serialise.__func__(field_definition, value)
        if not field_definition._deserialiser and issubclass(schema_type, SerialisableType):
            field_definition._deserialiser = lambda value: schema_type.deserialise.__func__(field_definition, value)

        if issubclass(schema_type, ValidatableType):
            field_definition._validator = lambda value: schema_type.validate.__func__(field_definition, value)

        schema[field_name] = field_definition

    return schema


class _Undefined:
    pass


UNDEFINED = _Undefined()


class Field:
    def __init__(  # type: ignore
        self,
        maximum: Union[int, float, Decimal] = None,
        minimum: Union[int, float, Decimal] = None,
        multiple_of: Union[int, float, Decimal] = None,
        string_format: Union[str, Format] = None,
        pattern: str = None,
        read_only: bool = None,
        write_only: bool = None,
        serialiser: Callable[[Any], Any] = lambda value: value,
        deserialiser: Callable[[Any], Any] = lambda value: value,
        default: Any = None,
        default_factory: Callable = UNDEFINED,  # type: ignore
        compare: bool = True,
        repr: bool = True,
        items: Union[Type, "Field", None] = None,
    ):
        self.minimum = minimum
        self.maximum = maximum
        self.multiple_of = multiple_of
        self.string_format = string_format
        self.pattern = pattern
        self.read_only = read_only
        self.write_only = write_only
        self.repr = repr
        self.compare = compare
        self.items = items

        self._default = default
        self._default_factory = default_factory
        self._deserialiser = deserialiser
        self._serialiser = serialiser
        self._type = None
        self._validator: Callable[[Any], Any] = lambda value: value

    @property
    def default(self) -> Any:
        if self._default_factory is not UNDEFINED:
            return self._default_factory()
        if self._default is not UNDEFINED:
            return self._default

        return UNDEFINED

    @property
    def type(self) -> Type[Any]:
        return self._type  # type: ignore

    def validate(self, value) -> Any:
        return self._validator(value)

    def serialise(self, value) -> Any:
        return self._serialiser(value)

    def deserialise(self, value) -> Any:
        return value


class Reference(Field):
    pass


class Schema(Iterable):
    def __init__(self, dataclass_type: Any):
        self.type = dataclass_type
        self.class_name = dataclass_type.__name__
        self._fields: OrderedDict = OrderedDict()

    def __setitem__(self, key: str, value: Field):
        self._fields[key] = value

    def __getitem__(self, key: str) -> Field:
        return self._fields[key]

    def __contains__(self, key: str) -> bool:
        return key in self._fields

    def __iter__(self):
        return iter(self._fields.items())  # type: ignore

    def validate(self, value: Dict[str, Any]) -> Any:
        if isinstance(value, self.type):  # self validation
            return value

        return value
