class ValidationError(ValueError):
    def __bool__(self):
        return False


__all__ = ["ValidationError"]
