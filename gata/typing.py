import uuid
from datetime import date, datetime, time, timedelta
from typing import Any, Pattern, Union

from typing_extensions import Protocol, runtime

from .errors import FormatValidationError, ValidationError
from .format import Format
from .iso_datetime import (
    parse_iso_date_string,
    parse_iso_datetime_string,
    parse_iso_duration_string,
    parse_iso_time_string,
    timedelta_to_iso_string,
)
from .validators import (
    TRUTHY_EXPRESSION,
    validate_boolean,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_email,
    validate_float,
    validate_hostname,
    validate_integer,
    validate_ipv4,
    validate_ipv6,
    validate_list,
    validate_multiple_of,
    validate_object_id,
    validate_range,
    validate_semver,
    validate_string,
    validate_time,
    validate_uri,
    validate_url,
    validate_uuid,
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
}


@runtime
class ValidatableType(Protocol):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return value


@runtime
class SerialisableType(Protocol):
    @classmethod
    def serialise(cls, value: Any) -> Any:
        return value

    @classmethod
    def deserialise(cls, value: Any) -> Any:
        return value


class ConstrainedBoolean(bool, ValidatableType, SerialisableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_boolean(value)

    @classmethod
    def serialise(cls, value: Any) -> Any:
        return value

    @classmethod
    def deserialise(cls, value: Any) -> Any:
        if value is False or value is True:
            return value
        if value in TRUTHY_EXPRESSION:
            return True
        return False


class ConstrainedInteger(int, ValidatableType):
    minimum: int
    maximum: int
    multiple_of: int

    @classmethod
    def validate(cls, value: Any) -> Any:
        value = validate_integer(value)
        validate_range(value, cls.minimum, cls.maximum)

        if cls.multiple_of:
            validate_multiple_of(value, cls.multiple_of)

        return value


class ConstrainedFloat(float, ValidatableType):
    minimum: float
    maximum: float
    multiple_of: float

    @classmethod
    def validate(cls, value: Any) -> Any:
        value = validate_float(value)
        validate_range(value, cls.minimum, cls.maximum)

        if cls.multiple_of:
            validate_multiple_of(value, cls.multiple_of)

        return value


class ConstrainedString(str, ValidatableType):
    minimum: int
    maximum: int
    pattern: Pattern[str]
    format: Format

    @classmethod
    def validate(cls, value: Any) -> Any:
        value = validate_string(value)

        if cls.format:
            _FORMAT_TO_VALIDATOR_MAP[cls.format](value)
        if cls.pattern and not cls.pattern.match(value):
            raise FormatValidationError(expected_format=cls.pattern)
        validate_range(value, cls.minimum, cls.maximum)

        return value


class ConstrainedList(list, ValidatableType, SerialisableType):
    minimum: int
    maximum: int
    items: Union[ValidatableType, SerialisableType]

    @classmethod
    def validate(cls, value: Any) -> Any:
        value = validate_list(value, cls.items.validate)
        validate_range(value, cls.minimum, cls.maximum)
        return value

    @classmethod
    def serialise(cls, value: Any) -> Any:
        result = []
        for item in value:
            result.append(cls.items.serialise(item))
        return result

    @classmethod
    def deserialise(cls, value: Any) -> Any:
        result = []
        for item in value:
            result.append(cls.items.deserialise(item))
        return result


class EmailAddress(str, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_email(value)


class Duration(timedelta, SerialisableType, ValidatableType):
    minimum: timedelta
    maximum: timedelta

    @classmethod
    def validate(cls, value: Any) -> Any:
        try:
            parse_iso_duration_string(value)
        except ValueError:
            raise ValidationError("Passed value must be valid ISO-8601 duration expression.")

        validate_range(value, cls.minimum, cls.maximum)
        return value

    @classmethod
    def serialise(cls, value: Any) -> str:
        return timedelta_to_iso_string(value)

    @classmethod
    def deserialise(cls, value: Any) -> timedelta:
        return parse_iso_duration_string(value)


class URI(str, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_uri(value)


class UrlAddress(str, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_url(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "url"})


class Hostname(str, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_hostname(value)


class Semver(str, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_semver(value)


class UUID(uuid.UUID, SerialisableType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_uuid(value)

    @classmethod
    def serialise(cls, value: Any) -> str:
        return str(value)

    @classmethod
    def deserialise(cls, value: Any) -> uuid.UUID:
        return uuid.UUID(value)


class Date(date, SerialisableType, ValidatableType):
    minimum: date
    maximum: date

    @classmethod
    def validate(cls, value: Any) -> Any:
        value = validate_date(value)
        validate_range(value, cls.minimum, cls.maximum)

        return value

    @classmethod
    def serialise(cls, value: Any) -> str:
        return value.isoformat()

    @classmethod
    def deserialise(cls, value: Any) -> date:
        return parse_iso_date_string(value)


class DateTime(datetime, SerialisableType, ValidatableType):
    minimum: datetime
    maximum: datetime

    @classmethod
    def validate(cls, value: Any) -> Any:
        value = validate_datetime(value)
        validate_range(value, cls.minimum, cls.maximum)

        return value

    @classmethod
    def serialise(cls, value: Any) -> str:
        return value.isoformat()

    @classmethod
    def deserialise(cls, value: Any) -> datetime:
        return parse_iso_datetime_string(value)


class Time(time, SerialisableType, ValidatableType):
    minimum: time
    maximum: time

    @classmethod
    def validate(cls, value: Any) -> Any:
        value = validate_time(value)
        validate_range(value, cls.minimum, cls.maximum)

        return value

    @classmethod
    def serialise(cls, value: Any) -> str:
        return value.isoformat()

    @classmethod
    def deserialise(cls, value: Any) -> time:
        return parse_iso_time_string(value)
