from typing_extensions import Protocol, runtime_checkable
from typing import Dict, Any, ItemsView, Union, Callable, Optional
from gata.schema import Schema, build_schema, UNDEFINED, Field, Reference
from decimal import Decimal
from gata.format import Format


@runtime_checkable
class Dataclass(Protocol):  # pragma: no cover
    __gata_schema__: Schema
    __frozen_dict__: Dict[str, Any]

    def serialise(self, **mapping) -> Dict[str, Any]:
        ...

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        ...

    def __iter__(self) -> ItemsView[str, Any]:
        ...


def _dataclass_method_serialise(self: "Dataclass", **mapping) -> Dict[str, Any]:
    self.__gata_schema__


def _dataclass_method_validate(_cls: "Dataclass", value: Dict[str, Any]) -> None:
    _cls.__gata_schema__.validate(value)


def _dataclass_method_iter(self: "Dataclass") -> ItemsView[str, Any]:
    for key, value in self.serialise().items():
        yield key, value


def _dataclass_method_repr(self: "Dataclass") -> str:
    fields_repr = ", ".join(
        [f"{name}={getattr(self, name)!r}" for name, field_schema in self.__gata_schema__ if field_schema.repr]
    )

    return f"{self.__class__.__qualname__}({fields_repr})"


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
    raise TypeError(f"cannot modify attribute {name} of {self}, the dataclass is marked as frozen")


def _dataclass_method_frozen_getattr(self: "Dataclass", name: str) -> Any:
    if name in self.__frozen_dict__:
        return self.__frozen_dict__[name]
    raise TypeError(f"cannot get non existing attribute {name} of {self}, the dataclass is marked as frozen")


def _deserialise_field_from_hash(property_name: str, property_descriptor: Field, object_hash: Dict[str, Any]) -> Any:
    if property_name not in object_hash:
        default_value = property_descriptor.default
        if default_value is UNDEFINED:
            return None

        return default_value

    value = object_hash[property_name]
    if property_descriptor._deserialiser:
        return property_descriptor._deserialiser(value, property_descriptor.type)

    return value  # deserialise_type(value, property_descriptor.type)


# lets create frozen method init and normal, and also frozen wrapped init
def _dataclass_method_init(__frozen__: bool, __validate__: bool, *args, **kwargs) -> None:
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

    if __validate__:
        self.validate(init_kwargs)
    frozen_dict = {}
    for property_name, property_descriptor in self.__gata_schema__:  # type: ignore
        if property_descriptor.read_only:
            continue

        value = _deserialise_field_from_hash(property_name, property_descriptor, init_kwargs)
        if __frozen__:
            frozen_dict[property_name] = value
            continue
        setattr(self, property_name, value)

    if __frozen__:
        self.__dict__["__frozen_dict__"] = frozen_dict

    if "__post_init__" in self.__dict__:
        self.__post_init__()


def _process_class(
    _cls: Optional[Any] = None,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    validate=True,
) -> "Dataclass":
    if order or unsafe_hash:
        raise NotImplementedError(
            "order and unsafe_hash attributes are not yet supported. If you need those features please use python's dataclasses instead"
        )

    if not hasattr(_cls, "__gata_schema__"):
        build_schema(_cls)

    setattr(_cls, "validate", _dataclass_method_validate)
    setattr(_cls, "serialise", _dataclass_method_serialise)
    setattr(_cls, "__iter__", _dataclass_method_iter)

    if repr and "__repr__" not in _cls.__dict__:
        setattr(_cls, "__repr__", _dataclass_method_repr)

    if eq and "__eq__" not in _cls.__dict__:
        setattr(_cls, "__eq__", _dataclass_method_eq)

    if frozen:
        setattr(_cls, "__setattr__", _dataclass_method_frozen_setattr)
        setattr(_cls, "__getattr__", _dataclass_method_frozen_getattr)

    if not init:
        if frozen:
            raise ValueError(f"cannot define dataclass {_cls} as frozen when init=False")
        return _cls

    __init__ = object.__init__
    if "__init__" in _cls.__dict__:
        __init__ = getattr(_cls, "__init__")

    setattr(_cls, "__init__", _dataclass_method_init)

    return _cls


def serialise_mapped_field(
    result: Dict[str, Any], key: str, value: Any, schema_field: Field, mapping: Dict[str, Union[bool, str, dict]]
) -> None:
    item_key = mapping[key]
    serialised_value = schema_field.serialise(value)

    if isinstance(item_key, str):
        result[item_key] = serialised_value
        return None

    if isinstance(item_key, bool):
        if not item_key:
            return None
        result[key] = serialised_value
        return None

    raise ValueError(f"unsupported mapping option for key {key}, mapping supports boo, str, dict, callable values only")


def serialise_dataclass(
    obj: Any, mapping: Optional[Dict[str, Union[str, bool, Dict[str, Any]]]] = None
) -> Dict[str, Any]:
    if hasattr(obj, "__gata_schema__"):
        schema = obj.__gata_schema__
    else:
        schema = build_schema(obj.__class__)

    result = {}

    for key, field in schema:
        if field.write_only:
            continue
        value = getattr(obj, key) if hasattr(obj, key) else UNDEFINED

        if mapping and key in mapping:
            serialise_mapped_field(result, key, value, field, mapping)
            continue

        if value is UNDEFINED:
            result[key] = None
            continue

        if isinstance(field, Reference):
            result[key] = serialise_dataclass(value)
            continue

        result[key] = field.serialise(value)

    return result


def dataclass(
    _cls: Optional[Any] = None,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
    validate=True,
) -> Union[Callable[[Any], "Dataclass"], "Dataclass"]:
    def _dataclass(cls: Any) -> Dataclass:
        return _process_class(cls, init, repr, eq, order, unsafe_hash, frozen, validate)

    if _cls is None:
        return _dataclass

    return _dataclass(_cls)


def field(
    default: Any = UNDEFINED,
    default_factory: Any = UNDEFINED,
    init: bool = True,
    repr: bool = True,
    hash: None = None,
    compare: bool = True,
    metadata: None = None,
    maximum: Union[int, float, Decimal] = None,
    minimum: Union[int, float, Decimal] = None,
    multiple_of: Union[int, float, Decimal] = None,
    string_format: Union[str, Format] = None,
    pattern: str = None,
    read_only: bool = None,
    write_only: bool = None,
) -> Field:
    if hash or metadata or init is False:
        raise NotImplementedError(
            "hash and metadata attribute are not yet supported. If you need these feature please use python's dataclasses instead"
        )

    return Field(
        default=default,
        repr=repr,
        compare=compare,
        default_factory=default_factory,
        minimum=minimum,
        maximum=maximum,
        multiple_of=multiple_of,
        string_format=string_format,
        pattern=pattern,
        read_only=read_only,
        write_only=write_only,
    )
