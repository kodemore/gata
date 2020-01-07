import re

from gata.errors import ValidationError

_IPV4_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$", re.I
)


def validate_ipv4(value: str) -> bool:
    if not _IPV4_REGEX.match(value):
        raise ValidationError(f"Passed value {value} is not valid ipv4 address.")

    return True


__all__ = ["validate_ipv4"]
