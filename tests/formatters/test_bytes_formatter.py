from gata.formatters import Base64Formatter


def test_hydrate_bytes_string() -> None:
    result = Base64Formatter.hydrate("dGVzdCBzdHJpbmc=")

    assert isinstance(result, bytes)
    assert result.decode("utf8") == "test string"


def test_extract_bytes_string() -> None:
    result = Base64Formatter.extract("test string".encode("utf-8"))
    assert isinstance(result, str)
    assert result == "dGVzdCBzdHJpbmc="
