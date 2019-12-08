import base64
import binascii
from typing import Any

from .formatter import Formatter


class Base64Formatter(Formatter):
    @classmethod
    def hydrate(cls, value: str) -> Any:
        try:
            decoded_value = base64.b64decode(value)
        except binascii.Error:
            raise ValueError("Passed value is not valid base64 encoded string.")

        return decoded_value

    @classmethod
    def extract(cls, value: bytes) -> str:
        return base64.b64encode(value).decode("utf8")


__all__ = ["Base64Formatter"]
