from gata.types.object import Object


def is_dataclass(python_type) -> bool:
    return (
        "__dataclass__" in python_type.__dict__
        and isinstance(python_type.__dict__["__dataclass__"], Object)
        and "validate" in python_type.__dict__
    )


__all__ = ["is_dataclass"]
