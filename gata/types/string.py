from typing import Any

from gata import validators
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


class StringType(Type):
    def __init__(self):
        super().__init__()
        self._allow_overrides += (
            "min_length",
            "max_length",
            "pattern",
            "format",
        )
        self.min_length = None
        self.max_length = None
        self.pattern = None
        self.format = None

    def validate(self, value: Any) -> None:
        if self.min_length is not None or self.max_length is not None:
            validators.validate_length(value, self.min_length, self.max_length)

        if self.format in FORMAT_TO_VALIDATOR_MAP:
            validate_value = FORMAT_TO_VALIDATOR_MAP[self.format]
            validate_value(value)  # type: ignore

    def __getitem__(self, item: Format) -> "StringType":
        return self.__call__(format=item)


String = StringType()

__all__ = ["String", "Format"]
