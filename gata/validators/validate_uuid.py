import re

from gata.errors import ValidationError

_UUID_REGEX = re.compile(
    r"^(?:urn:uuid:)?[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$", re.I
)


def validate_uuid(value: str) -> bool:
    if not _UUID_REGEX.match(value):
        raise ValidationError(f"Passed value {value} is not valid uuid.")

    return True


__all__ = ["validate_uuid"]
