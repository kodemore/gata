from gata.types.object import Object


def is_dataclass(python_type) -> bool:
    if "__schema__" in python_type.__dict__ and \
            isinstance(python_type.__dict__["__schema__"], Object) and \
            "validate" in python_type.__dict__:
        return True

    return False


__all__ = ["is_dataclass"]
