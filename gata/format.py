from enum import Enum

# Format has to stay as separate module to deal with cyclomatic dependencies.


class Format(Enum):
    DATETIME = "date-time"
    DATE = "date"
    TIME = "time"
    URI = "uri"
    URL = "url"
    EMAIL = "email"
    UUID = "uuid"
    HOSTNAME = "hostname"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    BOOLEAN = "boolean"
    SEMVER = "semver"
    BYTE = "byte"
    BASE64ULR = "base64url"
    DURATION = "duration"
    BSON_OBJECT_ID = "bson-object-id"


__all__ = ["Format"]
