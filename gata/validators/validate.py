from collections.abc import Sequence as BaseSequence
from enum import Enum
from inspect import isclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import TypeVar
from typing import Union

from gata.errors import ValidationError
from gata.types.type import Type


def validate(value: Any, type_definition: Union[type, Any]) -> None:

    if isinstance(type_definition, Type):
        type_definition.validate(value)
        return

    if not check_type(value, type_definition):
        raise ValidationError(
            f"Passed value {value} does not conform specified type {type_definition}."
        )


def check_type(value: Any, type_definition: Union[type, Any]) -> bool:
    if type_definition is Any:
        return True

    if type_definition is None:
        return value is None

    origin_type = getattr(type_definition, "__origin__", None)
    if origin_type is None:
        if issubclass(type_definition, Enum):  # type: ignore
            return check_enum(value, type_definition)

        if isclass(type_definition):
            return isinstance(value, type_definition)  # type: ignore
        else:
            return False

    if origin_type not in ORIGIN_TYPE_TO_VALIDATOR_MAP:
        return False

    origin_validator: Callable = ORIGIN_TYPE_TO_VALIDATOR_MAP[origin_type]

    return origin_validator(value, type_definition)


def check_enum(value: Any, type_definition: Union[type, Any]) -> bool:
    if isinstance(value, type_definition):
        return True
    values = set(item.value for item in type_definition)  # type: ignore

    return value in values


def check_dict(value: Any, type_definition: Union[type, Any]) -> bool:
    if not isinstance(value, dict):
        return False
    key_type, value_type = type_definition.__args__  # type: ignore

    if isinstance(key_type, TypeVar) and isinstance(  # type: ignore
        value_type, TypeVar  # type: ignore
    ):
        return True

    for item_key, item_value in value.items():
        if not check_type(item_key, key_type) or not check_type(item_value, value_type):
            return False

    return True


def check_list(value: Any, type_definition: Union[type, Any]) -> bool:
    if not isinstance(value, list):
        return False
    (value_type,) = type_definition.__args__  # type: ignore

    if isinstance(value_type, TypeVar):  # type: ignore
        return True

    for item_value in value:
        if not check_type(item_value, value_type):
            return False

    return True


def check_sequence(value: Any, type_definition: Union[type, Any]) -> bool:
    if not isinstance(value, Sequence):
        return False

    (value_type,) = type_definition.__args__  # type: ignore
    if isinstance(value_type, TypeVar):  # type: ignore
        return True

    for item_value in value:
        if not check_type(item_value, value_type):
            return False

    return True


def check_set(value: Any, type_definition: Union[type, Any]) -> bool:
    if not isinstance(value, set):
        return False

    (value_type,) = type_definition.__args__  # type: ignore
    if isinstance(value_type, TypeVar):  # type: ignore
        return True

    for item_value in value:
        if not check_type(item_value, value_type):
            return False

    return True


def check_tuple(value: Any, type_definition: Union[type, Any]) -> bool:
    if not isinstance(value, tuple):
        return False

    if type_definition.__args__:  # type: ignore
        (value_type,) = type_definition.__args__  # type: ignore
    else:
        return True

    if isinstance(value_type, TypeVar):  # type: ignore
        return True

    for item_value in value:
        if not check_type(item_value, value_type):
            return False

    return True


def check_union(value: Any, type_definition: Union[type, Any]) -> bool:
    union_params = type_definition.__args__  # type: ignore
    for subtype_definition in union_params:
        if check_type(value, subtype_definition):
            return True
    return False


ORIGIN_TYPE_TO_VALIDATOR_MAP = {
    dict: check_dict,
    Dict: check_dict,
    list: check_list,
    List: check_list,
    Sequence: check_sequence,
    BaseSequence: check_sequence,
    set: check_set,
    Set: check_set,
    tuple: check_tuple,
    Tuple: check_tuple,
    Union: check_union,
}


__all__ = ["validate", "check_type"]
