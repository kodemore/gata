from typing import Union, Callable

from gata.format import Format
from gata.validators.validate_base64 import validate_base64
from gata.validators.validate_date import validate_date
from gata.validators.validate_datetime import validate_datetime
from gata.validators.validate_email import validate_email
from gata.validators.validate_falsy import validate_falsy
from gata.validators.validate_hostname import validate_hostname
from gata.validators.validate_ipv4 import validate_ipv4
from gata.validators.validate_ipv6 import validate_ipv6
from gata.validators.validate_semver import validate_semver
from gata.validators.validate_time import validate_time
from gata.validators.validate_truthy import validate_truthy
from gata.validators.validate_uri import validate_uri
from gata.validators.validate_url import validate_url
from gata.validators.validate_uuid import validate_uuid

FORMAT_TO_VALIDATOR_MAP = {
    Format.DATETIME: validate_datetime,
    Format.DATE: validate_date,
    Format.TIME: validate_time,
    Format.URI: validate_uri,
    Format.URL: validate_url,
    Format.EMAIL: validate_email,
    Format.UUID: validate_uuid,
    Format.HOSTNAME: validate_hostname,
    Format.IPV4: validate_ipv4,
    Format.IPV6: validate_ipv6,
    Format.TRUTHY: validate_truthy,
    Format.FALSY: validate_falsy,
    Format.SEMVER: validate_semver,
    Format.BYTE: validate_base64,
}

STRING_FORMAT_TO_FORMAT_MAP = {
    "datetime": validate_datetime,
    "date": validate_date,
    "time": validate_time,
    "uri": validate_uri,
    "url": validate_url,
    "email": validate_email,
    "uuid": validate_uuid,
    "hostname": validate_hostname,
    "ipv4": validate_ipv4,
    "ipv6": validate_ipv6,
    "truthy": validate_truthy,
    "falsy": validate_falsy,
    "semver": validate_semver,
    "byte": validate_base64,
}


def validate_format(value: str, format: Union[str, Format]) -> bool:

    if isinstance(format, str) and format in STRING_FORMAT_TO_FORMAT_MAP:
        validate = STRING_FORMAT_TO_FORMAT_MAP[format]  # type: function
    elif isinstance(format, Format):
        validate = FORMAT_TO_VALIDATOR_MAP[format]
    else:
        return False

    return validate(value)  # type: ignore


__all__ = ["validate_format"]
