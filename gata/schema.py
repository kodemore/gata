from collections import OrderedDict
from collections.abc import Iterable
from decimal import Decimal
from inspect import isclass
from typing import Any, Callable, Dict, Optional, Union, Iterator, Tuple

from .mapping import Mapping, AnyTypeMapping
from .stringformat import StringFormat
from .utils import is_optional_type


class _Undefined:
    pass


UNDEFINED = _Undefined()


class Field:
    def __init__(  # type: ignore
        self,
        maximum: Union[int, float, Decimal] = None,
        minimum: Union[int, float, Decimal] = None,
        multiple_of: Union[int, float, Decimal] = None,
        string_format: Union[str, StringFormat] = None,
        pattern: str = None,
        read_only: bool = False,
        write_only: bool = False,
        serialiser: Optional[Callable[[Any, Optional[Dict[str, Any]]], Any]] = None,
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
        self._validator = validator

        self._original_type: Any = None
        self._is_optional: Optional[bool] = None
        self._type: Mapping = AnyTypeMapping()

    @property
    def is_optional(self) -> bool:
        if self._is_optional is None:
            self._is_optional = is_optional_type(self._original_type) or self.default is not UNDEFINED

        return self._is_optional

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
        if isclass(self._original_type) and isinstance(value, self._original_type):
            return value
        if self._deserialiser:
            return self._deserialiser(value)

        return self._type.deserialise(value)


class Schema(Iterable):
    def __init__(self, dataclass_type: Any):
        self.type = dataclass_type
        self.class_name = dataclass_type.__name__
        self._fields: OrderedDict = OrderedDict()

    def __setitem__(self, key: str, value: Field) -> None:
        self._fields[key] = value

    def __getitem__(self, key: str) -> Field:
        return self._fields[key]

    def __contains__(self, key: str) -> bool:
        return key in self._fields

    def __iter__(self) -> Iterator[Tuple[str, Field]]:
        for key, value in self._fields.items():
            yield key, value
