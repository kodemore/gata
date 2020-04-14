import uuid
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Any

from typing_extensions import Protocol, runtime

from .errors import ValidationError
from .utils import (
    parse_iso_date_string,
    parse_iso_datetime_string,
    parse_iso_duration_string,
    parse_iso_time_string,
    timedelta_to_iso_string,
)
from .validators import (
    validate_date,
    validate_datetime,
    validate_email,
    validate_hostname,
    validate_semver,
    validate_time,
    validate_uri,
    validate_url,
    validate_uuid,
)


@runtime
class ValidatableType(Protocol):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return value


@runtime
class SerialisableType(Protocol):
    @classmethod
    def serialise(cls, value: Any):
        return value

    @classmethod
    def deserialise(cls, value: Any):
        return value


@runtime
class SchemaType(Protocol):
    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        ...


class EmailAddress(str, SerialisableType, ValidatableType, SchemaType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_email(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "email"})


@dataclass
class Duration(timedelta, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        try:
            parse_iso_duration_string(value)
        except ValueError:
            raise ValidationError("Passed value must be valid ISO-8601 duration expression.")

        return value

    @classmethod
    def serialise(cls, value: Any) -> str:
        return timedelta_to_iso_string(value)

    @classmethod
    def deserialise(cls, value: Any) -> timedelta:
        return parse_iso_duration_string(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "duration"})


class URI(str, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_uri(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "uri"})


class UrlAddress(str, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_url(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "url"})


class Hostname(str, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_hostname(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "hostname"})


class Semver(str, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_semver(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "semver"})


class UUID(uuid.UUID, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_uuid(value)

    @classmethod
    def serialise(cls, value: Any) -> str:
        return str(value)

    @classmethod
    def deserialise(cls, value: Any) -> uuid.UUID:
        return uuid.UUID(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "uuid"})


class Date(date, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_date(value)

    @classmethod
    def serialise(cls, value: Any) -> str:
        return value.isoformat()

    @classmethod
    def deserialise(cls, value: Any) -> date:
        return parse_iso_date_string(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "date"})


class DateTime(datetime, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_datetime(value)

    @classmethod
    def serialise(cls, value: Any) -> str:
        return value.isoformat()

    @classmethod
    def deserialise(cls, value: Any) -> datetime:
        return parse_iso_datetime_string(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "date-time"})


class Time(time, SerialisableType, SchemaType, ValidatableType):
    @classmethod
    def validate(cls, value: Any) -> Any:
        return validate_time(value)

    @classmethod
    def serialise(cls, value: Any) -> str:
        return value.isoformat()

    @classmethod
    def deserialise(cls, value: Any) -> time:
        return parse_iso_time_string(value)

    @classmethod
    def update_schema(cls, field_schema: dict) -> None:
        field_schema.update({"format": "time"})
