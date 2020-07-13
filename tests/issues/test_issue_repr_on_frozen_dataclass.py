from gata import dataclass


def test_repr_on_frozen_dataclass() -> None:
    @dataclass(frozen=True)
    class A:
        a: str
        b: str

    a = A("a", "b")
    a_repr = repr(a)
    assert a.a == "a"
    assert a.b == "b"
    assert "test_repr_on_frozen_dataclass.<locals>.A" in a_repr
