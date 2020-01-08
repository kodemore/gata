from gata import Validator


def test_call_validator() -> None:
    assert Validator.email("test@gmail.com")


def test_decorate() -> None:

    @validate(email=)
    def some_sanitize_function(email: str) -> None:
        pass
