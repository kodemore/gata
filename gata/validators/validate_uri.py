import re

from gata.errors import ValidationError

_URI_REGEX = re.compile(r"^(?:[a-z][a-z0-9+-.]*:)(?:\\/?\\/)?[^\s]*$", re.I)


def validate_uri(value: str) -> None:
    if not _URI_REGEX.match(value):
        raise ValidationError(f"Passed value {value} is not valid uri.")


__all__ = ["validate_uri"]
