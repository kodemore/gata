from dataclasses import field, is_dataclass
from typing import Any, Callable, Dict, Generator, Type, TypeVar, Union

from typing_extensions import Protocol, runtime_checkable

from .deserialise import deserialise as deserialise_type, deserialise_dataclass
from .schema import Field, UNDEFINED, get_dataclass_schema, is_gataclass
from .serialise import serialise_dataclass

T = TypeVar("T")


@runtime_checkable
class Validatable(Protocol):  # pragma: no cover
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        ...


@runtime_checkable
class Serialisable(Protocol):  # pragma: no cover
    @classmethod
    def deserialise(cls, data: Dict[str, Any]) -> T:
        ...

    def serialise(self, **mapping) -> Dict[str, Any]:
        ...


def serialise(value: Any, mapping: Dict[str, Union[str, bool, dict, Callable]] = None) -> Union[Any, Dict[str, Any]]:
    dataclass_class = type(value)
    if not is_dataclass(dataclass_class) and not is_gataclass(dataclass_class):
        raise ValueError(f"passed `value` {value!r} must be instance of dataclass.")

    return serialise_dataclass(value, dataclass_class, mapping)


def deserialise(value: dict, target_class: Any) -> Any:
    if not is_dataclass(target_class) and not is_gataclass(target_class):
        raise ValueError(f"passed `target_class` {target_class} must be valid dataclass")

    return deserialise_dataclass(value, target_class)


def _deserialise_field_from_hash(property_name: str, property_descriptor: Field, object_hash: Dict[str, Any]) -> Any:
    if property_name not in object_hash:
        default_value = property_descriptor.default
        if default_value is UNDEFINED:
            return None

        return default_value

    value = object_hash[property_name]
    if property_descriptor.deserialiser:
        return property_descriptor.deserialiser(value, property_descriptor.type)

    return deserialise_type(value, property_descriptor.type)


def _frozen_setattr(self, name: str, value: Any) -> None:
    raise TypeError(f"cannot modify attribute {name} of {self}, the dataclass is marked as frozen")


def _frozen_getattr(self, name: str) -> Any:
    if name in self.__frozen_dict__:
        return self.__frozen_dict__[name]
    raise TypeError(f"cannot get non existing attribute {name} of {self}, the dataclass is marked as frozen")


def _dataclass_repr(self) -> str:
    fields_repr = ", ".join(
        [f"{name}={getattr(self, name)!r}" for name, field_schema in get_dataclass_schema(self) if field_schema.repr]
    )

    return f"{self.__class__.__qualname__}({fields_repr})"


def _dataclass_eq(self, other: Type) -> bool:

    if self.__class__ is not other.__class__:
        return False

    for name, field_schema in get_dataclass_schema(self):
        if not field_schema.compare:
            continue

        if getattr(self, name) != getattr(other, name):
            return False

    return True


def dataclass(
    _cls: T = None, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, validate=True
) -> Union[T, Validatable, Serialisable, Callable[[T], Union[T, Validatable, Serialisable]]]:
    def _make_dataclass(_cls: T) -> Union[T, Validatable, Serialisable]:
        if order or unsafe_hash:
            raise NotImplementedError(
                "order and unsafe_hash attributes are not yet supported. If you need those features please use python's dataclasses instead"
            )

        schema = get_dataclass_schema(_cls)

        def _serialise(*args, **mapping) -> Dict[str, Any]:
            self = args[0]
            return serialise_dataclass(self, _cls, mapping)

        def _as_dict(*args) -> Generator:
            self = args[0]
            for key, value in serialise_dataclass(self, _cls).items():
                yield key, value

        setattr(_cls, "validate", lambda value: schema.validate(value))
        setattr(_cls, "serialise", _serialise)
        setattr(_cls, "__iter__", _as_dict)

        if repr and "__repr__" not in _cls.__dict__:
            setattr(_cls, "__repr__", _dataclass_repr)

        if eq and "__eq__" not in _cls.__dict__:
            setattr(_cls, "__eq__", _dataclass_eq)

        if frozen:
            setattr(_cls, "__setattr__", _frozen_setattr)
            setattr(_cls, "__getattr__", _frozen_getattr)

        if not init:
            if frozen:
                raise ValueError(f"cannot define dataclass {_cls} as frozen when init=False")
            return _cls

        __init__ = object.__init__
        if "__init__" in _cls.__dict__:
            __init__ = getattr(_cls, "__init__")

        def _init(*args, **kwargs) -> None:
            self = args[0]
            if __init__ != object.__init__:
                __init__(*args, **kwargs)
                return None

            init_kwargs = {}
            if len(args) > 1:
                index = 1
                for property_name, _ in schema:
                    init_kwargs[property_name] = args[index]
                    index += 1
                    if index >= len(args):
                        break

            init_kwargs = {**init_kwargs, **kwargs}

            if validate:
                schema.validate(init_kwargs)
            frozen_dict = {}
            for property_name, property_descriptor in schema:  # type: ignore
                if property_descriptor.read_only:
                    continue

                value = _deserialise_field_from_hash(property_name, property_descriptor, init_kwargs)
                if frozen:
                    frozen_dict[property_name] = value
                    continue
                setattr(self, property_name, value)

            if frozen:
                self.__dict__["__frozen_dict__"] = frozen_dict

            if "__post_init__" in self.__dict__:
                self.__post_init__()

        setattr(_cls, "__init__", _init)

        return _cls

    if _cls is None:
        return _make_dataclass

    return _make_dataclass(_cls)


__all__ = ["serialise", "deserialise", "dataclass", "Serialisable", "Validatable", "field"]
