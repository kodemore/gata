import base64
import re
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from ipaddress import AddressValueError, IPv4Address, IPv6Address
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Optional,
    Pattern,
    Set,
    Sized,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from uuid import UUID

from bson import ObjectId

from gata.format import Format
from .errors import (
    ArithmeticValidationError,
    FormatValidationError,
    IterableValidationError,
    MaximumBoundError,
    MaximumLengthError,
    MinimumBoundError,
    MinimumLengthError,
    TypeValidationError,
    UniqueValidationError,
    ValidationError,
)
from .utils import (
    Comparable,
    parse_iso_date_string,
    parse_iso_datetime_string,
    parse_iso_duration_string,
    parse_iso_time_string,
)

T = TypeVar("T")


def validate_all(value: Any, validators: Iterable[Callable]) -> Any:
    for validate in validators:
        value = validate(value)
    return value


def validate_string(value: Any) -> str:
    if isinstance(value, str):
        return value

    raise TypeValidationError(value=value, expected_type=str)


def validate_any(value: Any, validators: Iterable[Callable]) -> Any:
    for validate in validators:
        try:
            validate(value)
            return value
        except ValueError:
            continue

    raise ValidationError("Value could not be validated", code="any_error")


def validate_iterable(value: Any, item_validator: Callable = None, unique: bool = False) -> Collection[Any]:
    if not isinstance(value, Collection) or isinstance(value, str) or isinstance(value, dict):
        raise IterableValidationError()

    if isinstance(value, Sized) and unique and not len(set(value)) == len(value):
        raise UniqueValidationError()

    if item_validator:
        return validate_iterable_items(value, item_validator)  # type: ignore

    return value


def validate_iterable_items(
    value: Union[list, set, frozenset], item_validator: Callable
) -> Union[list, set, frozenset]:
    validated_items = []
    for item in value:
        validated_items.append(item_validator(item))

    if isinstance(value, set):
        return set(validated_items)

    if isinstance(value, frozenset):
        return frozenset(validated_items)

    return validated_items


def validate_list(value: Any, item_validator: Callable = None) -> List[Any]:
    if not isinstance(value, list):
        raise TypeValidationError(expected_type=list)

    if item_validator:
        return validate_iterable_items(value, item_validator)  # type: ignore

    return value  # type: ignore


def validate_set(value: Any, item_validator: Callable = None) -> Set[Any]:
    if not isinstance(value, set):
        raise TypeValidationError(expected_type=set)

    if item_validator:
        return validate_iterable_items(value, item_validator)  # type: ignore

    return value


def validate_tuple(value: Any, item_validators: List[Callable]) -> Tuple[Any, ...]:
    if not isinstance(value, tuple):
        raise TypeValidationError(expected_type=tuple)

    if item_validators:
        result = []
        index = 0
        for validator in item_validators:
            result.append(validator(value[index]))
            index += 1
        return tuple(result)

    return value


def validate_frozenset(value: Any, item_validator: Callable = None) -> FrozenSet[Any]:
    if not isinstance(value, frozenset):
        raise TypeValidationError(expected_type=frozenset)

    if item_validator:
        return validate_iterable_items(value, item_validator)  # type: ignore

    return value


def validate_pattern(value: Any) -> Pattern[str]:
    try:
        return re.compile(value)
    except Exception:
        raise TypeValidationError(expected_type=Pattern)


def validate_bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)

    return validate_base64(value)


def validate_base64(value: Any) -> bytes:
    try:
        return base64.b64decode(value)
    except Exception:
        pass

    raise TypeValidationError(expected_type=bytes)


FALSY_EXPRESSION = {0, "0", "no", "n", "nope", "false", "f", "off"}
TRUTHY_EXPRESSION = {1, "1", "ok", "yes", "y", "yup", "true", "t", "on"}


def validate_boolean(value: Any) -> bool:
    if value is True or value is False:
        return value

    if value in FALSY_EXPRESSION:
        return False

    if value in TRUTHY_EXPRESSION:
        return True

    raise TypeValidationError(expected_type=bool)


def validate_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    value = str(value)
    try:
        return parse_iso_datetime_string(value)
    except ValueError:
        raise TypeValidationError(expected_type=datetime)


def validate_dict(value: Any, key_validator: Callable[..., Any], value_validator: Callable[..., Any]) -> dict:
    if not isinstance(value, dict):
        raise TypeValidationError(expected_type=dict)

    result = {}
    for item_key, item_value in value.items():
        result[key_validator(item_key)] = value_validator(item_value)

    return result


def validate_typed_dict(value: Any, validator_map: Dict[str, Callable[..., Any]]) -> dict:
    if not isinstance(value, dict):
        raise TypeValidationError(expected_type=dict)

    for key, validator in validator_map.items():
        validator(value[key] if key in value else None)

    return value


def validate_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    value = str(value)
    try:
        return parse_iso_date_string(value)
    except ValueError:
        raise TypeValidationError(expected_type=date)


def validate_time(value: Any) -> time:
    if isinstance(value, time):
        return value
    value = str(value)
    try:
        return parse_iso_time_string(value)
    except ValueError:
        raise TypeValidationError(expected_type=time)


def validate_duration(value: Any) -> timedelta:
    if isinstance(value, timedelta):
        return value
    try:
        return parse_iso_duration_string(value)
    except Exception:
        raise TypeValidationError(expected_type=timedelta)


# https://www.w3.org/TR/html5/forms.html#valid-e-mail-address
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
    re.I,
)


def validate_email(value: str) -> str:
    """
    Keep in mind this validator willfully violates RFC 5322, the best way to invalidate email address is to send
    a message and receive confirmation from the recipient.
    """
    if not EMAIL_REGEX.match(value):
        raise FormatValidationError(expected_format=Format.EMAIL)
    if ".." in value:
        raise FormatValidationError(expected_format=Format.EMAIL)

    return value


def validate_enum(value: Any, enum_class: Type[Enum]) -> Enum:
    try:
        return enum_class(value)
    except ValueError:
        raise TypeValidationError(expected_type=enum_class)


HOSTNAME_REGEX = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[-0-9a-z]{0,61}[0-9a-z])?)*$", re.I)


def validate_hostname(value: str) -> str:
    if not HOSTNAME_REGEX.match(value):
        raise FormatValidationError(expected_format=Format.HOSTNAME)

    return value


def validate_integer(value: Any) -> int:
    if isinstance(value, int) and value is not True and value is not False:
        return value

    raise TypeValidationError(expected_type=int)


def validate_float(value: Any) -> float:
    if isinstance(value, float):
        return value

    raise TypeValidationError(expected_type=float)


def validate_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value

    try:
        value = Decimal(value)
        if not value.is_finite():
            raise TypeValidationError(expected_type=Decimal)

    except Exception:
        raise TypeValidationError(expected_type=Decimal)

    return value


def validate_ipv4(value: Any) -> IPv4Address:
    try:
        return IPv4Address(value)
    except AddressValueError:
        raise FormatValidationError(expected_format=Format.IPV4)


def validate_ipv6(value: Any) -> IPv6Address:
    try:
        return IPv6Address(value)
    except AddressValueError:
        raise FormatValidationError(expected_format=Format.IPV6)


def validate_length(value: Any, minimum: Optional[int] = None, maximum: Optional[int] = None) -> Any:
    length = len(value)

    if minimum is not None and length < minimum:
        raise MinimumLengthError(expected_minimum=minimum)

    if maximum is not None and length > maximum:
        raise MaximumLengthError(expected_maximum=maximum)

    return value


def validate_multiple_of(value: Union[float, int], multiple_of: Union[float, int]) -> Union[float, int]:
    if not value % multiple_of == 0:
        raise ArithmeticValidationError(
            f"Passed value must be multiplication of {multiple_of}", code="multiple_of_error"
        )

    return value


def validate_nullable(value: Any, validator: Callable) -> Any:
    if value is None:
        return None

    return validator(value)


def validate_range(value: Any, minimum: Optional[Comparable] = None, maximum: Optional[Comparable] = None) -> Any:

    if minimum is not None and value < minimum:
        raise MinimumBoundError(expected_minimum=minimum)

    if maximum is not None and value > maximum:
        raise MaximumBoundError(expected_maximum=maximum)

    return value


SEMVER_REGEX = re.compile(
    r"^((([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9a-z-]+(?:\.[0-9a-z-]+)*))?)(?:\+([0-9a-z-]+(?:\.[0-9a-z-]+)*))?)$", re.I
)


def validate_semver(value: Any) -> str:
    value = validate_string(value)
    if not SEMVER_REGEX.match(value):
        raise FormatValidationError(expected_format=Format.SEMVER)

    return value


URI_REGEX = re.compile(r"^(?:[a-z][a-z0-9+-.]*:)(?:\\/?\\/)?[^\s]*$", re.I)


def validate_uri(value: Any) -> str:
    value = validate_string(value)
    if not URI_REGEX.match(value):
        raise FormatValidationError(expected_format=Format.URI)

    return value


URL_REGEX = re.compile(
    r"^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9_]+-?)*[a-z\u00a1-\uffff0-9_]+)(?:\.(?:[a-z\u00a1-\uffff0-9_]+-?)*[a-z\u00a1-\uffff0-9_]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$",
    re.I | re.U,
)


def validate_url(value: Any) -> str:
    value = validate_string(value)
    if not URL_REGEX.match(value):
        raise FormatValidationError(expected_format=Format.URL)

    return value


def validate_object_id(value: Any) -> ObjectId:
    try:
        return ObjectId(value)
    except ValueError:
        raise FormatValidationError(expected_format=Format.BSON_OBJECT_ID)


def validate_uuid(value: Any) -> UUID:
    try:
        return UUID(value)
    except ValueError:
        raise FormatValidationError(expected_format=Format.UUID)


def validate_literal(value: Any, literal_type: Type) -> Any:
    if value in literal_type.__args__:
        return value
    raise ValidationError(f"Passed value must be within listed literals.", code="literal_error")


__all__ = [
    "validate_all",
    "validate_any",
    "validate_iterable",
    "validate_base64",
    "validate_boolean",
    "validate_bytes",
    "validate_datetime",
    "validate_date",
    "validate_dict",
    "validate_duration",
    "validate_typed_dict",
    "validate_decimal",
    "validate_email",
    "validate_enum",
    "validate_float",
    "validate_frozenset",
    "validate_hostname",
    "validate_integer",
    "validate_ipv4",
    "validate_ipv6",
    "validate_iterable_items",
    "validate_length",
    "validate_list",
    "validate_literal",
    "validate_multiple_of",
    "validate_nullable",
    "validate_object_id",
    "validate_pattern",
    "validate_range",
    "validate_semver",
    "validate_set",
    "validate_string",
    "validate_time",
    "validate_tuple",
    "validate_uri",
    "validate_url",
    "validate_uuid",
]
