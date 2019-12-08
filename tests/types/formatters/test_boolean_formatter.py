from gata.types.formatters import BooleanFormatter
import pytest


@pytest.mark.parametrize(
    "input,expected",
    [
        ("1", True),
        ("ok", True),
        ("yes", True),
        ("y", True),
        ("yup", True),
        ("true", True),
        ("on", True),
        ("0", False),
        ("no", False),
        ("n", False),
        ("nope", False),
        ("false", False),
        ("off", False),
    ],
)
def test_hydrate_boolean_string(input, expected) -> None:
    assert BooleanFormatter.hydrate(input) == expected


def test_extract_boolean_string() -> None:
    assert "true" == BooleanFormatter.extract(True)
    assert "false" == BooleanFormatter.extract(False)
