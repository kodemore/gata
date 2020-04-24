from gata import Validator


def test_assert() -> None:
    assert Validator.assert_integer(1)
    assert not Validator.assert_integer("fail")
