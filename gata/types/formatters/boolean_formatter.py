from typing import Any
from .formatter import Formatter


class BooleanFormatter(Formatter):
    @classmethod
    def hydrate(cls, value: str) -> Any:
        if isinstance(value, str):
            value = value.lower()
        if value in (0, 0.0, "0", False, "no", "n", "nope", "false", "off"):
            return False
        if value in (1, 1.0, "1", True, "ok", "yes", "y", "yup", "true", "on"):
            return True

        raise ValueError("Passed value cannot be formatted to boolean.")

    @classmethod
    def extract(cls, value: bool) -> str:
        return "yes" if value else "no"


__all__ = ["BooleanFormatter"]
