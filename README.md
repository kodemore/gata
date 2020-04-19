# Gata

[![CI](https://travis-ci.org/kodemore/gata.svg?branch=master)](https://travis-ci.org/kodemore/gata)
[![Coverage](https://codecov.io/gh/kodemore/gata/branch/master/graph/badge.svg)](https://codecov.io/gh/kodemore/gata)
[![Maintainability](https://api.codeclimate.com/v1/badges/00892e0c37a7f1716bdd/maintainability)](https://codeclimate.com/github/kodemore/gata/maintainability)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Gata is a toolbox library for python's dataclasses which allows to serialise/deserialise/validate complex dataclasses.

## Installation

`pip install gata`

## Features
 - non-intrusive interface
 - dataclasses validation mechanism
 - support for complex datatypes
 - serialisation/deserialisation mechanism
 - easy to use field mapping

<<<<<<< HEAD
=======
import gata


@dataclass
class Pet:
    name: str
    age: int = field(default=0)
    tags: List[str] = field(default_factory=list)
    sold_at: Optional[datetime] = field(default=None)

pet = Pet(name="Boo", age=10)

gata.serialise(pet)  # {"name": "Boo", "age": 10, "tags": [], "sold_at": None}
```

#### Mapping fields in the result
Serialise method can be fetched with additional `mapping` parameter which tells serialisation mechanism to rename fields
accordingly to set mapping rules in the returned result. Consider following example:
>>>>>>> c8998431775e1839fc923497046458acf76faa42

## Example
```python
<<<<<<< HEAD
=======
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import gata


@dataclass
class Pet:
    name: str
    age: int = field(default=0)
    tags: List[str] = field(default_factory=list)
    sold_at: Optional[datetime] = field(default=None)

pet = Pet(name="Boo", age=10)

gata.serialise(pet, mapping={
    "name": "pet_name", # name field will be mapped to `pet_name`
    "tags": False, # tags field will be excluded from serialisation
    # rest of the fields will be returned with names taken from dataclass
})
```

`mapping` argument must be a dict of `Dict[str, Union[str, bool, callable, dict]]` type. 

##### Mapping behaviour
When value is a `string`, field name will be simply mapped to corresponding key value.

When value is a `bool(False)` field will not be returned in the serialised value.

When value is a `callable`, value corresponding to mapped key will be passed to callable, which should return tuple.
First tuple's item will be used as a key for returned value and second is the value that will get returned as a part of serialised object.

Nested mapping is allowed, by passing `Dict[str, Union[str, bool, callable, dict]]` instance as a key value.

##### Nested mapping
```python
from dataclasses import dataclass
>>>>>>> c8998431775e1839fc923497046458acf76faa42
from typing import List
from gata import dataclass


@dataclass
class Pet:
    tags: List[str]
    name: str = "Boo"
    age: int = 0


try:
    pet = Pet()
except ValueError:
    pass  # tags are required and undefined, so error will be thrown


pet = Pet(**{"tags": ["dog"]})

assert pet.serialise() == {'tags': ['dog'], 'name': 'Boo', 'age': 0}  # serialise object

# exclude `age` field from serialisation, and rename `name` field to `pet_name`
assert pet.serialise(age=False, name="pet_name") == {'tags': ['dog'], 'pet_name': 'Boo'}
```

## Documentation

### [ Introduction](docs/1_introduction.md)

### [ Defining dataclass](docs/2_defining_dataclass.md)

  * [ Defining dataclass with python's native dataclass](docs/2_defining_dataclass.md#defining-dataclass-with-pythons-native-dataclass)
  * [ Defining dataclass with gata](docs/2_defining_dataclass.md#defining-dataclass-with-gata)
### [ Field types](docs/3_field_types.md)

  * [ Supported standard library types](docs/3_field_types.md#supported-standard-library-types)
    * [ Primitive types](docs/3_field_types.md#primitive-types)
    * [ Date-related types](docs/3_field_types.md#date-related-types)
    * [ Other standard library types](docs/3_field_types.md#other-standard-library-types)
    * [ Typing library](docs/3_field_types.md#typing-library)
    * [ Dataclasses](docs/3_field_types.md#dataclasses)
  * [ Gata types](docs/3_field_types.md#gata-types)
    * [ `gata.typing.EmailAddress`](docs/3_field_types.md#gatatypingemailaddress)
    * [ `gata.typing.Duration`](docs/3_field_types.md#gatatypingduration)
    * [ `gata.typing.URI`](docs/3_field_types.md#gatatypinguri)
    * [ `gata.typing.UrlAddress`](docs/3_field_types.md#gatatypingurladdress)
    * [ `gata.typing.Hostname`](docs/3_field_types.md#gatatypinghostname)
    * [ `gata.typing.Semver`](docs/3_field_types.md#gatatypingsemver)
    * [ `gata.typing.Uuid`](docs/3_field_types.md#gatatypinguuid)
    * [ `gata.typing.Date`](docs/3_field_types.md#gatatypingdate)
    * [ `gata.typing.DateTime`](docs/3_field_types.md#gatatypingdatetime)
    * [ `gata.typing.Time`](docs/3_field_types.md#gatatypingtime)
  * [ Defining custom types](docs/3_field_types.md#defining-custom-types)
### [ Validation](docs/4_validation.md)

  * [ Automatic validation](docs/4_validation.md#automatic-validation)
    * [ Performing post initialisation processing](docs/4_validation.md#performing-post-initialisation-processing)
  * [ Manual validation](docs/4_validation.md#manual-validation)
  * [ Extra validators](docs/4_validation.md#extra-validators)
### [ Deserialisation](docs/5_deserialisation.md)

  * [ Automatic deserialisation](docs/5_deserialisation.md#automatic-deserialisation)
  * [ Manual deserialisation](docs/5_deserialisation.md#manual-deserialisation)
  * [ Nested deserialisation](docs/5_deserialisation.md#nested-deserialisation)
### [ Serialisation](docs/6_serialisation.md)

  * [ Serialising gata's dataclasses](docs/6_serialisation.md#serialising-gatas-dataclasses)
  * [ Serialising python's dataclasses](docs/6_serialisation.md#serialising-pythons-dataclasses)
  * [ Mapping fields](docs/6_serialisation.md#mapping-fields)
* [ Turn off validation during instantiation](docs/6_serialisation.md#turn-off-validation-during-instantiation)
* [ file://examples/mapping_fields.py](docs/6_serialisation.md#fileexamplesmapping_fieldspy)
    * [ Nested mapping](docs/6_serialisation.md#nested-mapping)
* [ file://examples/nested_mapping_example.py](docs/6_serialisation.md#fileexamplesnested_mapping_examplepy)
### [ Detailed schema](docs/7_detailed_schemas.md)

  * [ `gata.Field` properties](docs/7_detailed_schemas.md#gatafield-properties)
    * [ Custom serialisers/deserialisers](docs/7_detailed_schemas.md#custom-serialisersdeserialisers)
