# Validation

## Automatic validation

`gata.dataclass` automatically adds `__init__` method to your class definition if none is defined.  
This method will accept only key/value arguments which SHOULD correspond to class' fields. When such a class
gets instantiated validation happens automatically. 

Consider the following example:
 
```python
from typing import List, Optional

from gata import dataclass, field
from gata.errors import FieldError


@dataclass
class Album:
    name: str
    artist: str
    release_year: int
    tags: Optional[List[str]] = field(default_factory=list)


try:
    invalid_release_year = Album(name="Perfect Strangers", artist="Deep Purple", release_year="1984")
except FieldError as error:
    print(f"there was an error with validating field: {error.context['field_name']}")

# file://examples/validating_gata_dataclass.py
```

Additionally the decorator appends `validate(value: dict) -> None` method to annotated class definition.
This method also can be used to validate input data.

> When dataclass defines its own `__init__` method `gata.dataclass` decorator will ensure it gets called
> and after that will run validation on newly created instance. This process is less efficient as it requires
> serialisation step. It is recommended to use `__post_init__` method if your class requires initialisation.


### Performing post initialisation processing

If your dataclass requires some additional post processing after instantiation you can declare `__post_init__(self) -> None`
method same way like it is done in python's `dataclasses` package. Consider the following example:

```python
from typing import List

from gata import dataclass


@dataclass
class Album:
    name: str
    artist: str
    songs: List[str]

    def __post_init__(self) -> None:
        self.songs_count = len(self.songs)


dict_album = {"name": "The Razor's Edge", "artist": "AC/DC", "songs": ["Thunderstruck", "Fire Your Guns"]}

album = Album(**dict_album)
print(album.songs_count)  # will print 2

# file://examples/post_init_example.py
```

## Manual validation

In case there is no control over source code and replacing `dataclasses.dataclass` decorator is not an option, 
`gata.validate` function can be used to check if instantiated dataclass is valid:

```python
from dataclasses import dataclass, field
from typing import List, Optional

from gata import validate
from gata.errors import FieldError


@dataclass
class Album:
    name: str
    artist: str
    release_year: int
    tags: Optional[List[str]] = field(default_factory=list)


try:
    album = Album(name="Perfect Strangers", artist="Deep Purple", release_year="1984")
    validate(album)
except FieldError as error:
    print(f"there was an error with validating field: {error.context['field_name']}")

# file://examples/validating_python_dataclass.py
```

## Extra validators

Gata also serves a static validator class for simple assertions, the following is a list of available assertions:
 - `gata.Validator.assert_array(value, items)` checks if value is set or list and each item conforms passed validator
 - `gata.Validator.assert_base64(value)` checks if passed string is valid base64 value
 - `gata.Validator.assert_date(value, min, max)` checks if passed string is valid iso date value
 - `gata.Validator.assert_datetime(value, min, max)` checks if passed string is valid iso datetime value
 - `gata.Validator.assert_email(value)` checks if passed string is valid email address
 - `gata.Validator.assert_falsy(value)` checks if passed string is valid falsy expression
 - `gata.Validator.assert_hostname(value)` checks if passed string is valid host name
 - `gata.Validator.assert_ipv4(value)` checks if passed string is valid ipv4 address
 - `gata.Validator.assert_ipv6(value)` checks if passed string is valid ipv6 address
 - `gata.Validator.assert_number(value, min, max, multiple_of)` checks if passed value is a valid number
 - `gata.Validator.assert_object_id(value)` checks if passed string is valid bson's object_id value
 - `gata.Validator.assert_semver(value)` checks if passed string is valid semantic versioning number
 - `gata.Validator.assert_time(value, min, max)` checks if passed string is valid iso time
 - `gata.Validator.assert_truthy(value)` checks if passed string is valid truthy expression
 - `gata.Validator.assert_uri(value)` checks if passed string is valid uri
 - `gata.Validator.assert_url(value)` checks if passed string is valid url
 - `gata.Validator.assert_uuid(value)` checks if passed string is valid uuid number

```python
from gata import Validator

assert Validator.assert_email("email@test.com")
assert Validator.assert_integer(12)
assert Validator.assert_duration("PT2H")

# file://examples/assertion_example.py
```
example.py
```
