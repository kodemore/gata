import base64
import binascii

from gata.errors import ValidationError


def validate_base64(value: str) -> bool:
    try:
        base64.b64decode(value)
    except binascii.Error:
        raise ValidationError("Passed value is not valid base64 encoded string.")

    return True


__all__ = ["validate_base64"]
