import numbers
from functools import partial
from typing import Any
from typing import Callable

from .utils.map_type_to_validator import map_type_to_validator
from .validators.validate_all import validate_all
from .validators.validate_array import validate_array
from .validators.validate_format import validate_format
from .validators.validate_length import validate_length
from .validators.validate_range import validate_range
from .validators.validate_multiple_of import validate_multiple_of


def _create_min_max_validator(field_type, meta: dict) -> Callable[..., bool]:
    min_max_kwargs = {
        "minimum": meta.get("min"),
        "maximum": meta.get("max"),
    }
    if field_type in (
        int,
        float,
        complex,
        numbers.Number,
        numbers.Real,
        numbers.Rational,
    ):
        return partial(validate_range, **min_max_kwargs)
    else:
        return partial(validate_length, **min_max_kwargs)


def _build_meta_validator(value_type, meta: dict) -> Callable[..., bool]:
    meta_validators = []
    if "min" in meta or "max" in meta:
        meta_validators.append(_create_min_max_validator(value_type, meta))

    if value_type is str and "format" in meta:
        meta_validators.append(partial(validate_format, format=meta["format"]))

    if "multiple_of" in meta:
        meta_validators.append(
            partial(validate_multiple_of, multiple_of=meta["multiple_of"])
        )

    origin_type = getattr(value_type, "__origin__", None)
    if origin_type and origin_type in (list, set) and "items" in meta:
        (item_type,) = value_type.__args__
        meta_validators.append(
            partial(
                validate_array, items=_build_meta_validator(item_type, meta["items"])
            )
        )

    def _validator(value: Any) -> bool:
        # None values should not be validated against meta
        if value is None:
            return True
        return partial(validate_all, validators=meta_validators)(value)

    return _validator


class FieldDescriptor:
    def __init__(self, field_type, field_meta: dict):
        self.type = field_type
        self.meta = field_meta
        self._validator = None

    @property
    def validator(self) -> Callable[..., bool]:
        if self._validator:
            return self._validator

        self._validator = partial(  # type: ignore
            validate_all,
            validators=[
                map_type_to_validator(self.type),
                _build_meta_validator(self.type, self.meta),
            ],
        )

        return self._validator  # type: ignore

    def validate(self, value: Any) -> bool:
        validator = self.validator
        return validator(value)


__all__ = ["FieldDescriptor"]
