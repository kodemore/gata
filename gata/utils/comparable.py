from typing import Any

from typing_extensions import Protocol
from typing_extensions import runtime


@runtime
class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...

    def __gt__(self, other: Any) -> bool:
        ...

    def __le__(self, other: Any) -> bool:
        return not self > other

    def __ge__(self, other: Any) -> bool:
        return not self < other


__all__ = ["Comparable"]
