import base64
import decimal
import ipaddress
import re
import uuid
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Pattern
from typing import TypeVar
from typing import Union

from gata import bson_support
from .base_mapping import Mapping
from .errors import FormatValidationError
from .errors import ValidationError
from .iso_datetime import parse_iso_date_string
from .iso_datetime import parse_iso_datetime_string
from .iso_datetime import parse_iso_duration_string
from .iso_datetime import parse_iso_time_string
from .iso_datetime import timedelta_to_iso_string
from .stringformat import StringFormat
from .validators import TRUTHY_EXPRESSION
from .validators import validate_any
from .validators import validate_boolean
from .validators import validate_bytes
from .validators import validate_date
from .validators import validate_datetime
from .validators import validate_decimal
from .validators import validate_email
from .validators import validate_enum
from .validators import validate_float
from .validators import validate_frozenset
from .validators import validate_hostname
from .validators import validate_integer
from .validators import validate_ipv4
from .validators import validate_ipv6
from .validators import validate_length
from .validators import validate_list
from .validators import validate_multiple_of
from .validators import validate_none
from .validators import validate_pattern
from .validators import validate_range
from .validators import validate_semver
from .validators import validate_set
from .validators import validate_string
from .validators import validate_time
from .validators import validate_tuple
from .validators import validate_uri
from .validators import validate_url
from .validators import validate_uuid

_FORMAT_TO_VALIDATOR_MAP = {
    StringFormat.DATETIME: validate_datetime,
    StringFormat.DATE: validate_date,
    StringFormat.TIME: validate_time,
    StringFormat.URI: validate_uri,
    StringFormat.URL: validate_url,
    StringFormat.EMAIL: validate_email,
    StringFormat.UUID: validate_uuid,
    StringFormat.HOSTNAME: validate_hostname,
    StringFormat.IPV4: validate_ipv4,
    StringFormat.IPV6: validate_ipv6,
    StringFormat.BOOLEAN: validate_boolean,
    StringFormat.SEMVER: validate_semver,
    StringFormat.BYTE: validate_bytes,
    "date-time": validate_datetime,
    "date": validate_date,
    "time": validate_time,
    "uri": validate_uri,
    "url": validate_url,
    "email": validate_email,
    "uuid": validate_uuid,
    "hostname": validate_hostname,
    "ipv4": validate_ipv4,
    "ipv6": validate_ipv6,
    "boolean": validate_boolean,
    "semver": validate_semver,
    "byte": validate_bytes,
}


T = TypeVar("T")

__all__ = [
    "Mapping",
    "BooleanMapping",
    "BytesMapping",
    "IntegerMapping",
    "FloatMapping",
    "StringMapping",
    "DecimalMapping",
    "TimedeltaMapping",
    "UUIDMapping",
    "DateMapping",
    "DateTimeMapping",
    "TimeMapping",
    "RegexPatternMapping",
    "Ipv4AddressMapping",
    "Ipv6AddressMapping",
    "ListMapping",
    "SetMapping",
    "TupleMapping",
    "AnyTypeMapping",
]


if bson_support.BSON_SUPPORT:
    _FORMAT_TO_VALIDATOR_MAP["object-id"] = bson_support.validate_object_id
    _FORMAT_TO_VALIDATOR_MAP[StringFormat.OBJECT_ID] = bson_support.validate_object_id
    __all__ = __all__ + ["ObjectIdMapping"]


class BooleanMapping(Mapping):
    def validate(self, value: Any) -> Any:
        return validate_boolean(value)

    def deserialise(self, value: Any) -> Any:
        if value is False or value is True:
            return value
        if value in TRUTHY_EXPRESSION:
            return True
        return False


class BytesMapping(Mapping):
    minimum: int
    maximum: int

    def validate(self, value: Any) -> Any:
        value = validate_bytes(value)
        validate_range(value, self.minimum, self.maximum)

        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return base64.b64encode(value).decode("utf8")

    def deserialise(self, value: Any) -> Any:
        if isinstance(value, bytes):
            return value
        if isinstance(value, bytearray):
            return bytes(value)
        if isinstance(value, str):
            return base64.b64decode(value)


class IntegerMapping(Mapping):
    minimum: int
    maximum: int
    multiple_of: int

    def validate(self, value: Any) -> Any:
        value = validate_integer(value)
        validate_range(value, self.minimum, self.maximum)

        if self.multiple_of:
            validate_multiple_of(value, self.multiple_of)

        return value


class FloatMapping(Mapping):
    minimum: float
    maximum: float
    multiple_of: float

    def validate(self, value: Any) -> Any:
        value = validate_float(value)
        validate_range(value, self.minimum, self.maximum)

        if self.multiple_of:
            validate_multiple_of(value, self.multiple_of)

        return value


class StringMapping(Mapping):
    minimum: int
    maximum: int
    pattern: Pattern[str]
    format: StringFormat

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.pattern and isinstance(self.pattern, str):
            self.pattern = re.compile(f"^{self.pattern}$")

    def validate(self, value: Any) -> Any:
        value = validate_string(value)

        if self.format:
            _FORMAT_TO_VALIDATOR_MAP[self.format](value)
        if self.pattern and not self.pattern.match(value):
            raise FormatValidationError(expected_format=self.pattern.pattern)

        validate_length(value, self.minimum, self.maximum)

        return value


class DecimalMapping(Mapping):
    minimum: decimal.Decimal
    maximum: decimal.Decimal

    def validate(self, value: Any) -> Any:
        value = validate_decimal(value)
        validate_range(value, self.minimum, self.maximum)
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return decimal.Decimal(value)


class TimedeltaMapping(Mapping):
    minimum: timedelta
    maximum: timedelta

    def validate(self, value: Any) -> Any:
        if not isinstance(value, timedelta):
            if not isinstance(value, str):
                raise ValidationError("Passed value must be valid ISO-8601 duration expression")
            try:
                value = parse_iso_duration_string(value)
            except ValueError:
                raise ValidationError("Passed value must be valid ISO-8601 duration expression.")

        validate_range(value, self.minimum, self.maximum)
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return timedelta_to_iso_string(value)

    def deserialise(self, value: Any) -> Any:
        return parse_iso_duration_string(value)


class UUIDMapping(Mapping):
    def validate(self, value: Any) -> Any:
        return validate_uuid(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return uuid.UUID(value)


class DateMapping(Mapping):
    minimum: date
    maximum: date

    def validate(self, value: Any) -> Any:
        value = validate_date(value)
        validate_range(value, self.minimum, self.maximum)

        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value.isoformat()

    def deserialise(self, value: Any) -> date:
        return parse_iso_date_string(value)


class DateTimeMapping(Mapping):
    minimum: datetime
    maximum: datetime

    def validate(self, value: Any) -> Any:
        value = validate_datetime(value)
        validate_range(value, self.minimum, self.maximum)

        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value.isoformat()

    def deserialise(self, value: Any) -> datetime:
        return parse_iso_datetime_string(value)


class TimeMapping(Mapping):
    minimum: time
    maximum: time

    def validate(self, value: Any) -> Any:
        value = validate_time(value)
        validate_range(value, self.minimum, self.maximum)

        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value.isoformat()

    def deserialise(self, value: Any) -> time:
        return parse_iso_time_string(value)


class RegexPatternMapping(Mapping):
    def validate(self, value: Any) -> Any:
        return validate_pattern(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value.pattern

    def deserialise(self, value: Any) -> Any:
        return re.compile(value)


class Ipv4AddressMapping(Mapping):
    def validate(self, value: Any) -> Any:
        return validate_ipv4(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return ipaddress.IPv4Address(value)


class Ipv6AddressMapping(Mapping):
    def validate(self, value: Any) -> Any:
        return validate_ipv6(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return ipaddress.IPv6Address(value)


def _serialise_iterable(
    value: Any, item_type: Optional[Mapping] = None, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None,
) -> List[Any]:
    result: List[Any] = []
    if not value:
        return result
    for item in value:
        if not mapping:
            result.append(item_type.serialise(item) if item_type else item)
            continue

        serialised_item = item_type.serialise(item, mapping=mapping) if item_type else item
        if "$item" in mapping:
            serialised_item = serialised_item[mapping["$item"]]
        result.append(serialised_item)
    return result


class ListMapping(Mapping):
    minimum: int
    maximum: int
    items: List[Mapping]

    def validate(self, value: Any) -> Any:
        value = validate_list(value, self.items[0].validate if self.items else None)

        validate_length(value, self.minimum, self.maximum)
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return _serialise_iterable(value, self.items[0] if self.items else None, mapping)

    def deserialise(self, value: Any) -> Any:
        result = []
        for item in value:
            result.append(self.items[0].deserialise(value=item))
        return result


class SetMapping(Mapping):
    minimum: int
    maximum: int
    items: Optional[List[Mapping]]

    def validate(self, value: Any) -> Any:
        value = validate_set(value, self.items[0].validate if self.items else None)

        validate_length(value, self.minimum, self.maximum)
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return _serialise_iterable(value, self.items[0] if self.items else None, mapping)

    def deserialise(self, value: Any) -> Any:
        if self.items:
            result = [self.items[0].deserialise(value=item) for item in value]
        else:
            result = value
        return set(result)


class FrozenSetMapping(Mapping):
    minimum: int
    maximum: int
    items: Optional[List[Mapping]]

    def validate(self, value: Any) -> Any:
        value = validate_frozenset(value, self.items[0].validate if self.items else None)

        validate_length(value, self.minimum, self.maximum)
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return _serialise_iterable(value, self.items[0] if self.items else None, mapping)

    def deserialise(self, value: Any) -> Any:
        if self.items:
            result = [self.items[0].deserialise(value=item) for item in value]
        else:
            result = value
        return frozenset(result)


class TupleMapping(Mapping):
    minimum: int
    maximum: int
    items: List[Union[Mapping, Any]]
    validators: List[Union[Callable, Any]]

    def validate(self, value: Any) -> Any:
        if not self.validators:
            self.validators = [item_type.validate for item_type in self.items if isinstance(item_type, Mapping)]
            if self.items[-1] is ...:
                self.validators.append(...)

        return validate_tuple(value, self.validators)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value

    def deserialise(self, value: Any) -> Any:
        return value


class UnionMapping(Mapping):
    items: List[Mapping]
    validators: List[Callable]

    def validate(self, value: Any) -> Any:
        if not self.validators:
            self.validators = [item_type.validate for item_type in self.items]

        return validate_any(value, self.validators)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value

    def deserialise(self, value: Any) -> Any:
        return value


class NoneMapping(Mapping):
    def validate(self, value: Any) -> Any:
        return validate_none(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return None

    def deserialise(self, value: Any) -> Any:
        return None


class GataclassMapping(Mapping):
    dataclass: Any

    def validate(self, value: Any) -> Any:
        if isinstance(value, self.dataclass):
            return value
        return self.dataclass(**value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        if mapping:
            return value.serialise(**mapping)
        return value.serialise()

    def deserialise(self, value: Any) -> Any:
        if isinstance(value, self.dataclass):
            return value
        return self.dataclass(**value)


class CustomTypeMapping(Mapping):
    custom_type: Any

    def validate(self, value: Any) -> Any:
        value = self.custom_type(value)
        value.validate()

        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value.serialise()

    def deserialise(self, value: Any) -> Any:
        return self.custom_type(value)


class EnumTypeMapping(Mapping):
    enum_type: Any

    def validate(self, value: Any) -> Any:
        return validate_enum(value, self.enum_type)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value.value

    def deserialise(self, value: Any) -> Any:
        return self.enum_type(value)


class AnyTypeMapping(Mapping):
    pass
