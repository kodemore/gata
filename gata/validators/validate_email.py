import re

from gata.errors import ValidationError

# https://www.w3.org/TR/html5/forms.html#valid-e-mail-address

_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
    re.I,
)


def validate_email(value: str) -> None:
    """
    Keep in mind this validator willfully violates RFC 5322, the best way to invalidate email address is to send
    a message and receive confirmation from the recipient.

    :param str value:
    :return None:
    """
    if not _EMAIL_REGEX.match(value):
        raise ValidationError(f"Passed value {value} is not valid email address.")
    if ".." in value:
        raise ValidationError(f"Passed value {value} is not valid email address.")


__all__ = ["validate_email"]
