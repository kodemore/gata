from gata import Validator


def test_call_validator() -> None:
    assert Validator.email("test@gmail.com")
