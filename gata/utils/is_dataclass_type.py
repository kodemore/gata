from inspect import isclass


def is_dataclass_type(python_type) -> bool:
    return (
        isclass(python_type)
        and "__dataclass__" in python_type.__dict__
        and isinstance(python_type.__dict__["__dataclass__"], dict)
        and "validate" in python_type.__dict__
    )


__all__ = ["is_dataclass_type"]
