import re

from gata.errors import ValidationError

_HOSTNAME_REGEX = re.compile(
    r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[-0-9a-z]{0,61}[0-9a-z])?)*$",
    re.I,
)


def validate_hostname(value: str) -> None:
    if not _HOSTNAME_REGEX.match(value):
        raise ValidationError(f"Passed value {value} is not valid hostname.")


__all__ = ["validate_hostname"]
