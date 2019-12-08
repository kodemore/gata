from typing import Any
from .formatter import Formatter


class BooleanFormatter(Formatter):
    @classmethod
    def hydrate(cls, value: str) -> Any:
        value = value.lower()

        if value in ("0", "no", "n", "nope", "false", "off"):
            return False
        if value in ("1", "ok", "yes", "y", "yup", "true", "on"):
            return True

        raise ValueError("Passed value cannot be formatted to boolean.")

    @classmethod
    def extract(cls, value: bool) -> str:
        return "true" if value else "false"


__all__ = ["BooleanFormatter"]
