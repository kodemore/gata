import datetime
import ipaddress
import uuid
from abc import ABC
from dataclasses import Field as DataclassesField
from decimal import Decimal
from enum import Enum
from inspect import isclass
from typing import Any
from typing import AnyStr
from typing import ByteString
from typing import Callable
from typing import Dict
from typing import ItemsView
from typing import Iterator
from typing import List
from typing import Optional
from typing import Pattern
from typing import Tuple
from typing import Type
from typing import Union

from gata import bson_support
from .errors import FieldError
from .errors import ValidationError
from .mapping import AnyTypeMapping
from .mapping import BooleanMapping
from .mapping import BytesMapping
from .mapping import CustomTypeMapping
from .mapping import DateMapping
from .mapping import DateTimeMapping
from .mapping import DecimalMapping
from .mapping import EnumTypeMapping
from .mapping import FloatMapping
from .mapping import GataclassMapping
from .mapping import IntegerMapping
from .mapping import Ipv4AddressMapping
from .mapping import Ipv6AddressMapping
from .mapping import ListMapping
from .mapping import NoneMapping
from .mapping import RegexPatternMapping
from .mapping import SetMapping
from .mapping import StringMapping
from .mapping import TimeMapping
from .mapping import TimedeltaMapping
from .mapping import TupleMapping
from .mapping import UUIDMapping
from .mapping import UnionMapping
from .schema import Field
from .schema import Schema
from .schema import UNDEFINED
from .stringformat import StringFormat
from .types import Type as CustomType
from .utils import NoneType
from .utils import is_dataclass_like


class Dataclass(ABC):  # pragma: no cover
    __gata_schema__: Schema
    __frozen_dict__: Dict[str, Any]
    __frozen__: bool
    __validate__: bool
    __class_name__: str

    def __init__(self, *args, **kwargs):
        ...

    def serialise(self, **mapping) -> Dict[str, Any]:
        ...

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        ...

    @classmethod
    def deserialise(cls, value: Dict[str, Any]) -> "Dataclass":
        ...

    def __iter__(self) -> ItemsView[str, Any]:
        ...

    def __post_init__(self) -> None:
        ...


def asdict(obj: Any, mapping: Dict[str, Union[bool, str, dict]] = {}) -> Dict[str, Any]:
    if not hasattr(obj.__class__, "__gata_schema__"):
        setattr(obj.__class__, "__gata_schema__", build_schema(obj.__class__))

    return _dataclass_method_serialise(obj, **mapping)


def _freeze_object(self: "Dataclass") -> None:
    frozen_dict = {}
    for property_name, property_schema in self.__gata_schema__:
        property_value = getattr(self, property_name)
        frozen_dict[property_name] = property_value
    self.__frozen_dict__ = frozen_dict


def validate_dataclass(obj: object) -> None:
    schema = build_schema(obj.__class__)
    for field_name, field_schema in schema:
        if field_schema.read_only:
            continue
        value = getattr(obj, field_name, None)
        if field_schema.is_optional and value is None:
            continue
        try:
            field_schema.validate(value)
        except ValidationError as error:
            raise FieldError(field_name, error) from error


def _dataclass_method_serialise(self, **mapping) -> Dict[str, Any]:
    serialised = {}
    for key, schema in self.__gata_schema__:
        if schema.write_only:
            continue
        value = getattr(self, key)
        if key not in mapping:
            serialised[key] = schema.serialise(value)
            continue

        serialise_mapped_field(serialised, key, value, schema, mapping)

    return serialised


def _dataclass_method_validate(cls: "Dataclass", value: Dict[str, Any]) -> None:
    for field_name, field_schema in cls.__gata_schema__:
        field_value = value[field_name] if field_name in value else None

        if field_value is None and field_schema.is_optional or field_schema.read_only:
            continue

        try:
            field_schema.validate(field_value)
        except ValidationError as error:
            raise FieldError(field_name, error) from error


def _dataclass_method_iter(self: "Dataclass") -> Iterator[Tuple[str, Any]]:
    for key, value in self.serialise().items():
        yield key, value


def _dataclass_method_repr(self: "Dataclass") -> str:
    fields_repr = ", ".join(
        [f"{name}={getattr(self, name)!r}" for name, field_schema in self.__gata_schema__ if field_schema.repr]
    )

    return f"{self.__class_name__}({fields_repr})"


def _dataclass_method_eq(self: "Dataclass", other: "Dataclass") -> bool:

    if self.__class__ is not other.__class__:
        return False

    for name, field_schema in self.__gata_schema__:
        if not field_schema.compare:
            continue

        if getattr(self, name) != getattr(other, name):
            return False

    return True


def _dataclass_method_frozen_setattr(self: "Dataclass", name: str, value: Any) -> None:
    if not self.__frozen_dict__:
        self.__dict__[name] = value
        return None
    raise TypeError(f"cannot modify attribute {name} of {self}, the dataclass is marked as frozen")


def _dataclass_method_frozen_getattr(self: "Dataclass", name: str) -> Any:
    if not self.__frozen_dict__:
        return self.__dict__.get(name)

    if name in self.__frozen_dict__:
        return self.__frozen_dict__[name]

    if name[0:2] == "__" and name[-2:] == "__":
        return super(self.__class__, self).__getattribute__(name)

    raise TypeError(f"cannot get non existing attribute {name} of {self}, the dataclass is marked as frozen")


def _deserialise_field_from_hash(property_name: str, property_descriptor: Field, object_hash: Dict[str, Any]) -> Any:
    if property_name not in object_hash:
        return property_descriptor.default if property_descriptor.default is not UNDEFINED else None

    value = object_hash[property_name]
    value = property_descriptor.deserialise(value)
    return value


def _dataclass_method_deserialise(cls, value: Dict[str, Any]):
    if not isclass(cls):
        self = cls
        cls = self.__class__
    else:
        self = cls.__new__(cls)

    if cls.__validate__:
        for property_name, field_schema in cls.__gata_schema__:
            property_value = value[property_name] if property_name in value else None

            if field_schema.is_optional or field_schema.read_only:
                if property_value is not None:
                    try:
                        property_value = field_schema.validate(property_value)
                    except ValidationError as error:
                        raise FieldError(property_name, error) from error
                else:
                    property_value = field_schema.default
                    if property_value is UNDEFINED:
                        property_value = None
            else:
                try:
                    property_value = field_schema.validate(property_value)
                except ValidationError as error:
                    raise FieldError(property_name, error) from error
            setattr(self, property_name, property_value)
    else:
        for property_name, property_descriptor in cls.__gata_schema__:  # type: ignore
            if property_descriptor.read_only:
                property_value = property_descriptor.default
                if property_value is UNDEFINED:
                    property_value = None
            else:
                property_value = _deserialise_field_from_hash(property_name, property_descriptor, value)
            setattr(self, property_name, property_value)

    return self


def _dataclass_method_init(*args, **kwargs) -> None:
    self: "Dataclass" = args[0]
    init_kwargs = {}
    if len(args) > 1:
        index = 1
        for property_name, _ in self.__gata_schema__:
            init_kwargs[property_name] = args[index]
            index += 1
            if index >= len(args):
                break

    init_kwargs = {**init_kwargs, **kwargs}

    self.deserialise.__func__(self, value=init_kwargs)  # type: ignore

    self.__post_init__()

    if self.__frozen__:
        _freeze_object(self)


def make_dataclass(_cls: Any, repr: bool = True, eq: bool = True, validate: bool = True, frozen: bool = False,) -> None:
    setattr(_cls, "validate", classmethod(_dataclass_method_validate))
    setattr(_cls, "deserialise", classmethod(_dataclass_method_deserialise))
    setattr(_cls, "serialise", _dataclass_method_serialise)
    setattr(_cls, "__iter__", _dataclass_method_iter)

    if repr:
        setattr(_cls, "__repr__", _dataclass_method_repr)

    if eq:
        setattr(_cls, "__eq__", _dataclass_method_eq)

    __init__ = object.__init__
    if "__init__" in _cls.__dict__:
        class_init = getattr(_cls, "__init__")

        def __init__(self, *args, **kwargs):
            class_init(self, *args, **kwargs)
            self.__post_init__()
            if validate:
                validate_dataclass(self)
            if frozen:
                _freeze_object(self)

    else:
        __init__ = _dataclass_method_init

    setattr(_cls, "__init__", __init__)

    if frozen:
        setattr(_cls, "__frozen_dict__", {})
        setattr(_cls, "__setattr__", _dataclass_method_frozen_setattr)
        setattr(_cls, "__getattr__", _dataclass_method_frozen_getattr)


def _process_class(
    _cls: Any, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, validate=True,
) -> Type["Dataclass"]:
    if order or unsafe_hash:
        raise NotImplementedError(
            "order and unsafe_hash attributes are not yet supported. If you need those features please use python's dataclasses instead"
        )

    if hasattr(_cls, "__gata_schema__"):
        schema = _cls.__gata_schema__  # type: ignore
    else:
        schema = build_schema(_cls)

    new_cls: Type["Dataclass"] = type(
        _cls.__name__ + "Dataclass",
        (_cls, Dataclass)
        if Dataclass not in _cls.__mro__[-1:0:-1]
        else tuple([_cls]),  # add Dataclass to bases only if its not there already
        {
            "__validate__": validate,
            "__frozen__": frozen,
            "__gata_schema__": schema,
            "__class_name__": _cls.__qualname__,
        },
    )

    if "__init__" in _cls.__dict__:
        setattr(new_cls, "__init__", _cls.__init__)

    make_dataclass(
        new_cls,
        repr=(repr and "__repr__" not in _cls.__dict__),
        eq=(eq and "__eq__" not in _cls.__dict__),
        frozen=frozen,
        validate=validate,
    )

    return new_cls


def serialise_mapped_field(
    result: Dict[str, Any], key: str, value: Any, schema_field: Field, mapping: Dict[str, Union[bool, str, dict]],
) -> None:
    item_key = mapping[key]
    serialised_value = schema_field.serialise(value, item_key)  # type: ignore

    if isinstance(item_key, str):
        result[item_key] = serialised_value
        return None

    if isinstance(item_key, bool):
        if not item_key:
            return None
        result[key] = serialised_value
        return None

    if isinstance(item_key, dict):
        if "$self" in item_key:
            result[item_key["$self"]] = serialised_value
            return None
        result[key] = serialised_value
        return None

    raise ValueError(f"unsupported mapping option for key {key}, mapping supports bool, str or dict values")


def dataclass(
    _cls: Optional[Any] = None,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    validate=True,
) -> Union[Callable[[Any], Type["Dataclass"]], Type["Dataclass"]]:
    def _dataclass(cls: Any) -> Type[Dataclass]:
        return _process_class(cls, init, repr, eq, order, unsafe_hash, frozen, validate)

    if _cls is None:
        return _dataclass

    return _dataclass(_cls)


def field(
    default: Any = UNDEFINED,
    default_factory: Any = UNDEFINED,
    repr: bool = True,
    hash: None = None,
    init: bool = True,
    compare: bool = True,
    metadata: None = None,
    maximum: Union[int, float, Decimal] = None,
    minimum: Union[int, float, Decimal] = None,
    multiple_of: Union[int, float, Decimal] = None,
    string_format: Union[str, StringFormat] = None,
    pattern: str = None,
    read_only: bool = False,
    write_only: bool = False,
    items: Optional[Dict[str, Any]] = None,
) -> Field:
    if hash or metadata:
        raise NotImplementedError(
            "hash and metadata attribute are not yet supported. If you need these feature please use python's dataclasses instead"
        )

    return Field(
        repr=repr,
        compare=compare,
        default=default,
        init=init,
        default_factory=default_factory,
        minimum=minimum,
        maximum=maximum,
        multiple_of=multiple_of,
        string_format=string_format,
        pattern=pattern,
        read_only=read_only,
        write_only=write_only,
        items=items if items else {},
    )


SUPPORTED_TYPES = {
    bool: BooleanMapping,
    int: IntegerMapping,
    float: FloatMapping,
    str: StringMapping,
    bytes: BytesMapping,
    bytearray: BytesMapping,
    list: ListMapping,
    set: SetMapping,
    tuple: TupleMapping,
    NoneType: NoneMapping,  # type: ignore
    List: ListMapping,
    Union: UnionMapping,
    Decimal: DecimalMapping,
    datetime.date: DateMapping,
    datetime.datetime: DateTimeMapping,
    datetime.time: TimeMapping,
    datetime.timedelta: TimedeltaMapping,
    getattr(Pattern, "__origin__"): RegexPatternMapping,
    ipaddress.IPv4Address: Ipv4AddressMapping,
    ipaddress.IPv6Address: Ipv6AddressMapping,
    uuid.UUID: UUIDMapping,
    Any: AnyTypeMapping,
    ByteString: BytesMapping,
    AnyStr: StringMapping,
}

if bson_support.BSON_SUPPORT:
    import bson

    SUPPORTED_TYPES[bson.ObjectId] = bson_support.ObjectIdMapping


def map_property_type_to_schema_type(property_type: Any, type_properties: Dict[str, Any]) -> Any:
    if isclass(property_type) and issubclass(property_type, Dataclass):
        return GataclassMapping(dataclass=property_type)

    if property_type in SUPPORTED_TYPES:
        return SUPPORTED_TYPES[property_type](**type_properties)

    origin_type = getattr(property_type, "__origin__", None)
    if origin_type is None:
        if property_type in SUPPORTED_TYPES:
            return SUPPORTED_TYPES[property_type](**type_properties)
        if isclass(property_type):
            if issubclass(property_type, CustomType):
                return CustomTypeMapping(custom_type=property_type)
            if issubclass(property_type, Enum):
                return EnumTypeMapping(enum_type=property_type)

        return AnyTypeMapping()
    if origin_type not in SUPPORTED_TYPES:
        return AnyTypeMapping()

    subtypes = []
    for python_subtype in property_type.__args__:
        if python_subtype is ...:
            subtypes.append(...)
            continue
        subtypes.append(
            map_property_type_to_schema_type(
                python_subtype, type_properties["items"] if "items" in type_properties else {},
            )
        )

    init_args = {**type_properties, **{"items": subtypes}}

    return SUPPORTED_TYPES[origin_type](**init_args)


def build_schema(_cls: Any) -> Schema:
    if not is_dataclass_like(_cls):
        raise ValueError(f"passed value {_cls} is not valid dataclass type")

    schema = Schema(_cls)
    for field_name, field_type in _cls.__annotations__.items():
        field_descriptor = Field()

        if hasattr(_cls, field_name):
            field_value = getattr(_cls, field_name)
            if isinstance(field_value, DataclassesField):
                field_descriptor.compare = field_value.compare
                field_descriptor.repr = field_value.repr
                field_descriptor._default = field_value.default
                field_descriptor._default_factory = field_value.default_factory  # type: ignore
            elif isinstance(field_value, Field):
                field_descriptor = field_value
            else:
                field_descriptor._default = field_value

        field_descriptor._original_type = field_type

        field_properties = {
            "minimum": field_descriptor.minimum,
            "maximum": field_descriptor.maximum,
            "multiple_of": field_descriptor.multiple_of,
            "format": field_descriptor.format,
            "items": field_descriptor.items,
            "pattern": field_descriptor.pattern,
        }

        field_descriptor._type = map_property_type_to_schema_type(field_type, field_properties)

        schema[field_name] = field_descriptor

    return schema
