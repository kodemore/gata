from gata.formatters import DateFormatter
import pytest
from datetime import date


@pytest.mark.parametrize(
    "input, expected_value",
    [("2010-10-21", date(2010, 10, 21)), ("20101021", date(2010, 10, 21))],
)
def test_date_formatter_hydrate(input, expected_value):

    formatted_value = DateFormatter.hydrate(input)
    assert isinstance(formatted_value, date)
    assert formatted_value == expected_value


@pytest.mark.parametrize("input", ["2010-10-41", "20102121"])
def test_fail_format_date(input):

    with pytest.raises(ValueError):
        DateFormatter.hydrate(input)


@pytest.mark.parametrize("input, expected_value", [(date(2010, 10, 21), "2010-10-21")])
def test_date_formatter_extract(input, expected_value):
    assert DateFormatter.extract(input) == expected_value
