import re
from typing import Any
from typing import Optional
from typing import Union

from gata import validators
from gata.errors import ValidationError
from gata.types.formatters.format import Format
from .type import Type

FORMAT_TO_VALIDATOR_MAP = {
    Format.DATETIME: validators.validate_datetime,
    Format.DATE: validators.validate_date,
    Format.TIME: validators.validate_time,
    Format.URI: validators.validate_uri,
    Format.URL: validators.validate_url,
    Format.EMAIL: validators.validate_email,
    Format.UUID: validators.validate_uuid,
    Format.HOSTNAME: validators.validate_hostname,
    Format.IPV4: validators.validate_ipv4,
    Format.IPV6: validators.validate_ipv6,
    Format.TRUTHY: validators.validate_truthy,
    Format.FALSY: validators.validate_falsy,
    Format.SEMVER: validators.validate_semver,
    Format.BYTE: validators.validate_base64,
}

STRING_FORMAT_TO_FORMAT_MAP = {
    "date-time": Format.DATETIME,
    "date": Format.DATE,
    "time": Format.TIME,
    "uri": Format.URI,
    "url": Format.URL,
    "email": Format.EMAIL,
    "uuid": Format.UUID,
    "hostname": Format.HOSTNAME,
    "ipv4": Format.IPV4,
    "ipv6": Format.IPV6,
    "truthy": Format.TRUTHY,
    "falsy": Format.FALSY,
    "semver": Format.SEMVER,
    "byte": Format.BYTE,
}


class StringType(Type):
    def __init__(self, string_format: Union[str, Format, None] = None):
        super().__init__()
        self.min_length: Optional[int] = None
        self.max_length: Optional[int] = None
        self.pattern = None
        self._format = None
        self.format = string_format  # type: ignore

    @property
    def format(self) -> Optional[Format]:
        return self._format

    @format.setter
    def format(self, value: Union[str, Format, None]) -> None:
        if isinstance(value, str):
            if value in STRING_FORMAT_TO_FORMAT_MAP:
                self._format = STRING_FORMAT_TO_FORMAT_MAP[value]
            else:
                raise ValueError(f"Unknown string format passed: {value}")
        elif isinstance(value, Format):
            self._format = value
        elif value is None:
            self._format = None
        else:
            raise ValueError(f"Unknown string format passed: {value}")

    def __call__(
        self,
        deprecated: bool = False,
        write_only: bool = False,
        read_only: bool = False,
        nullable: bool = False,
        default: Any = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        string_format: Union[str, Format, None] = None,
    ) -> "Type":
        instance: StringType = super().__call__(  # type: ignore
            deprecated, write_only, read_only, nullable, default
        )
        instance.min_length = min_length
        instance.max_length = max_length
        if pattern:
            instance.pattern = re.compile(pattern)  # type: ignore
        instance.format = string_format  # type: ignore

        return instance

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Passed value is not a valid string value.")

        if self.min_length is not None or self.max_length is not None:
            validators.validate_length(value, self.min_length, self.max_length)

        if self.format in FORMAT_TO_VALIDATOR_MAP:
            validate_value = FORMAT_TO_VALIDATOR_MAP[self.format]
            validate_value(value)  # type: ignore
        elif self.pattern:
            if not self.pattern.match(value):
                raise ValidationError(
                    f"Passed string does not conform pattern {self.pattern}"
                )

    def __getitem__(self, item: Format) -> "StringType":
        instance: StringType = self.__call__(string_format=item)  # type: ignore

        return instance


String = StringType()

__all__ = ["String", "Format", "StringType"]
