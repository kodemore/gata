from abc import ABC
import base64
from datetime import date, datetime, time, timedelta
import decimal
import ipaddress
import re
from typing import Any, Dict, Optional, Pattern, TypeVar, Union, List as PythonList
import uuid

import bson

from gata.errors import FormatValidationError, ValidationError
from gata.format import Format
from gata.iso_datetime import (
    parse_iso_date_string,
    parse_iso_datetime_string,
    parse_iso_duration_string,
    parse_iso_time_string,
    timedelta_to_iso_string,
)
from gata.validators import (
    TRUTHY_EXPRESSION,
    validate_boolean,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_decimal,
    validate_email,
    validate_float,
    validate_hostname,
    validate_integer,
    validate_ipv4,
    validate_ipv6,
    validate_list,
    validate_multiple_of,
    validate_object_id,
    validate_pattern,
    validate_range,
    validate_semver,
    validate_string,
    validate_time,
    validate_uri,
    validate_url,
    validate_uuid,
    validate_length,
)

_FORMAT_TO_VALIDATOR_MAP = {
    Format.DATETIME: validate_datetime,
    Format.DATE: validate_date,
    Format.TIME: validate_time,
    Format.URI: validate_uri,
    Format.URL: validate_url,
    Format.EMAIL: validate_email,
    Format.UUID: validate_uuid,
    Format.HOSTNAME: validate_hostname,
    Format.IPV4: validate_ipv4,
    Format.IPV6: validate_ipv6,
    Format.BOOLEAN: validate_boolean,
    Format.SEMVER: validate_semver,
    Format.BYTE: validate_bytes,
    Format.OBJECT_ID: validate_object_id,
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
    "object-id": validate_object_id,
}

T = TypeVar("T")

__all__ = [
    "AbstractType",
    "Boolean",
    "Bytes",
    "Integer",
    "Float",
    "String",
    "Decimal",
    "Duration",
    "UUID",
    "Date",
    "DateTime",
    "Time",
    "RegexPattern",
    "Ipv4Address",
    "Ipv6Address",
    "ObjectId",
    "List",
    "AnyType",
]


class AbstractType(ABC):
    def __init__(self, **kwargs):
        if not hasattr(self, "__annotations__"):
            return

        for property_name, property_type in self.__annotations__.items():
            if property_name in kwargs:
                setattr(self, property_name, kwargs[property_name])
                continue
            setattr(self, property_name, None)

    def validate(self, value: Any) -> Any:
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value

    def deserialise(self, value: Any) -> Any:
        return value


class Boolean(AbstractType):
    def validate(self, value: Any) -> Any:
        return validate_boolean(value)

    def deserialise(self, value: Any) -> Any:
        if value is False or value is True:
            return value
        if value in TRUTHY_EXPRESSION:
            return True
        return False


class Bytes(AbstractType):
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


class Integer(AbstractType):
    minimum: int
    maximum: int
    multiple_of: int

    def validate(self, value: Any) -> Any:
        value = validate_integer(value)
        validate_range(value, self.minimum, self.maximum)

        if self.multiple_of:
            validate_multiple_of(value, self.multiple_of)

        return value


class Float(AbstractType):
    minimum: float
    maximum: float
    multiple_of: float

    def validate(self, value: Any) -> Any:
        value = validate_float(value)
        validate_range(value, self.minimum, self.maximum)

        if self.multiple_of:
            validate_multiple_of(value, self.multiple_of)

        return value


class String(AbstractType):
    minimum: int
    maximum: int
    pattern: Union[Pattern[str], str]
    format: Format

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


class Decimal(AbstractType):
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


class Duration(AbstractType):
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


class UUID(AbstractType):
    def validate(self, value: Any) -> Any:
        return validate_uuid(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return uuid.UUID(value)


class Date(AbstractType):
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


class DateTime(AbstractType):
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


class Time(AbstractType):
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


class RegexPattern(AbstractType):
    def validate(self, value: Any) -> Any:
        return validate_pattern(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return value.pattern

    def deserialise(self, value: Any) -> Any:
        return re.compile(value)


class Ipv4Address(AbstractType):
    def validate(self, value: Any) -> Any:
        return validate_ipv4(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return ipaddress.IPv4Address(value)


class Ipv6Address(AbstractType):
    def validate(self, value: Any) -> Any:
        return validate_ipv6(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return ipaddress.IPv6Address(value)


class ObjectId(AbstractType):
    def validate(self, value: Any) -> Any:
        return validate_object_id(value)

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        return str(value)

    def deserialise(self, value: Any) -> Any:
        return bson.ObjectId(value)


class List(AbstractType):
    minimum: int
    maximum: int
    items: Optional[PythonList[AbstractType]]

    def validate(self, value: Any) -> Any:
        value = validate_list(value, self.items[0].validate if self.items else None)

        validate_length(value, self.minimum, self.maximum)
        return value

    def serialise(self, value: Any, mapping: Optional[Dict[str, Union[Dict, str, bool]]] = None) -> Any:
        result = []
        for item in value:
            serialised_item = self.items[0].serialise(item, mapping=mapping)
            if "$item" in mapping:
                serialised_item = serialised_item[mapping["$item"]]
            result.append(serialised_item)
        return result

    def deserialise(self, value: Any) -> Any:
        result = []
        for item in value:
            result.append(self.items[0].deserialise(item))
        return result


class AnyType(AbstractType):
    pass
