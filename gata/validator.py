from .validators import (
    validate_all,
    validate_any,
    validate_boolean,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_decimal,
    validate_email,
    validate_enum,
    validate_float,
    validate_frozenset,
    validate_hostname,
    validate_integer,
    validate_ipv4,
    validate_ipv6,
    validate_iterable,
    validate_iterable_items,
    validate_length,
    validate_list,
    validate_literal,
    validate_multiple_of,
    validate_nullable,
    validate_pattern,
    validate_range,
    validate_semver,
    validate_set,
    validate_string,
    validate_time,
    validate_tuple,
    validate_uri,
    validate_url,
    validate_uuid,
)


class Validator:
    all = validate_all
    any = validate_any
    array = validate_iterable
    boolean = validate_boolean
    bytes = validate_bytes
    datetime = validate_datetime
    date = validate_date
    decimal = validate_decimal
    email = validate_email
    enum = validate_enum
    float = validate_float
    frozenset = validate_frozenset
    hostname = validate_hostname
    integer = validate_integer
    ipv4 = validate_ipv4
    ipv6 = validate_ipv6
    items = validate_iterable_items
    length = validate_length
    list = validate_list
    literal = validate_literal
    multiple_of = validate_multiple_of
    nullable = validate_nullable
    pattern = validate_pattern
    range = validate_range
    semver = validate_semver
    set = validate_set
    string = validate_string
    time = validate_time
    tuple = validate_tuple
    uri = validate_uri
    url = validate_url
    uuid = validate_uuid


__all__ = ["Validator"]
