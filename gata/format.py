from enum import Enum


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


__all__ = ["Format"]
