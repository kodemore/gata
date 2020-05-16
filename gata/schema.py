from collections import OrderedDict
from collections.abc import Iterable
from decimal import Decimal
from typing import Any, Callable, Dict, Optional, Union

from gata.format import Format
from gata.typing import Type as GataType


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
        read_only: bool = False,
        write_only: bool = False,
        serialiser: Optional[Callable[[Any], Any]] = None,
        deserialiser: Optional[Callable[[Any], Any]] = None,
        validator: Optional[Callable[[Any], None]] = None,
        default: Any = UNDEFINED,
        default_factory: Callable = UNDEFINED,  # type: ignore
        compare: bool = True,
        repr: bool = True,
        items: Dict[str, Any] = {},
    ):
        self.minimum = minimum
        self.maximum = maximum
        self.multiple_of = multiple_of
        self.format = string_format
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
        self._validator: Callable = validator

        self._original_type: Any = None
        self._type: GataType = None

    @property
    def default(self) -> Any:
        if self._default_factory is not UNDEFINED:
            return self._default_factory()
        if self._default is not UNDEFINED:
            return self._default

        return UNDEFINED

    @property
    def type(self) -> Any:
        return self._original_type  # type: ignore

    def validate(self, value) -> Any:
        if self._validator:
            return self._validator(value)

        return self._type.validate(value)

    def serialise(self, value, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        if self._serialiser:
            return self._serialiser(value, mapping)

        return self._type.serialise(value, mapping)

    def deserialise(self, value) -> Any:
        if self._deserialiser:
            return self._deserialiser(value)

        return self._type.deserialise(value)


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
