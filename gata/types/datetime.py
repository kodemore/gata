from .string import Format
from .string import StringType

DateTime = StringType(Format.DATETIME)
Date = StringType(Format.DATE)
Time = StringType(Format.TIME)

__all__ = ["DateTime", "Date", "Time"]
