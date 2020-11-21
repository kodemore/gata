from inspect import isclass
from typing import Any
from typing import Union


def is_dataclass_like(obj: Any) -> bool:
    cls = obj if isinstance(obj, type) else type(obj)
    return isclass(cls) and hasattr(cls, "__annotations__")


def is_gataclass(obj: Any) -> bool:
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, "__gata_schema__")


def is_typed_dict(value: Any) -> bool:
    if issubclass(value, dict) and hasattr(value, "__annotations__"):
        return True

    return False


NoneType = type(None)


def is_optional_type(type_: Any) -> bool:
    origin_type = getattr(type_, "__origin__", None)

    if not origin_type:
        return False
    if origin_type != Union:
        return False

    return NoneType in type_.__args__  # type: ignore
