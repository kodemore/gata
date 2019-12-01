import re

from gata.errors import ValidationError

_SEMVER_REGEX = re.compile(
    r"^((([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9a-z-]+(?:\.[0-9a-z-]+)*))?)(?:\+([0-9a-z-]+(?:\.[0-9a-z-]+)*))?)$",
    re.I,
)


def validate_semver(value: str) -> None:
    if not _SEMVER_REGEX.match(value):
        raise ValidationError(
            f"Passed value {value} is not valid semantic version number."
        )


__all__ = ["validate_semver"]
