from .dataclass_error import DataClassError


class InvalidTypeError(DataClassError):
    pass


__all__ = ["InvalidTypeError"]
