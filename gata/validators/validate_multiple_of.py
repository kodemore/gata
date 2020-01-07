from gata.errors import ValidationError


def validate_multiple_of(value: float, multiple_of: float) -> bool:
    if not value % multiple_of == 0:
        raise ValidationError(
            f"Passed value `{value}` must be multiplication of {multiple_of}."
        )

    return True


__all__ = ["validate_multiple_of"]
