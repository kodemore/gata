class DataClassError(RuntimeError):
    def __bool__(self):
        return False


__all__ = ["DataClassError"]
