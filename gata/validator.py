from .validators.validate_array import validate_array
from .validators.validate_base64 import validate_base64
from .validators.validate_date import validate_date
from .validators.validate_datetime import validate_datetime
from .validators.validate_email import validate_email
from .validators.validate_falsy import validate_falsy
from .validators.validate_hostname import validate_hostname
from .validators.validate_ipv4 import validate_ipv4
from .validators.validate_ipv6 import validate_ipv6
from .validators.validate_semver import validate_semver
from .validators.validate_time import validate_time
from .validators.validate_truthy import validate_truthy
from .validators.validate_uri import validate_uri
from .validators.validate_url import validate_url
from .validators.validate_uuid import validate_uuid
from .validators.validate_number import validate_number


class Validator:
    array = validate_array
    base64 = validate_base64
    date = validate_date
    datetime = validate_datetime
    email = validate_email
    falsy = validate_falsy
    hostname = validate_hostname
    ipv4 = validate_ipv4
    ipv6 = validate_ipv6
    number = validate_number
    semver = validate_semver
    time = validate_time
    truthy = validate_truthy
    uri = validate_uri
    url = validate_url
    uuid = validate_uuid


__all__ = ["Validator"]
