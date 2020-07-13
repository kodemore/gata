# Gata

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
 - Full IDE support with `Dataclass` class


## Example
```python
from typing import List
from gata import Dataclass


class Pet(Dataclass, frozen=True):
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

## Non intrusive example
```python
from typing import List
from gata import validate_dataclass, asdict
from dataclasses import dataclass


@dataclass
class Pet:
    tags: List[str]
    name: str = "Boo"
    age: int = 0


try:
    pet = Pet()
    validate_dataclass(pet)
except ValueError:
    pass  # tags are required and undefined, so error will be thrown


pet = Pet(**{"tags": ["dog"]})

assert asdict(pet) == {'tags': ['dog'], 'name': 'Boo', 'age': 0}  # serialise object

# exclude `age` field from serialisation, and rename `name` field to `pet_name`
assert asdict(pet, {"age": False, "name": "pet_name"}) == {'tags': ['dog'], 'pet_name': 'Boo'}
```

> More examples are available under [examples](examples) directory

## Documentation

### [ Introduction](docs/1_introduction.md)

### [ Defining dataclass](docs/2_defining_dataclass.md)

### [ Field types](docs/3_field_types.md)

  * [ Supported standard library types](docs/3_field_types.md#supported-standard-library-types)
    * [ Primitive types](docs/3_field_types.md#primitive-types)
    * [ Date-related types](docs/3_field_types.md#date-related-types)
    * [ Other standard library types](docs/3_field_types.md#other-standard-library-types)
    * [ Typing library](docs/3_field_types.md#typing-library)
    * [ Dataclasses](docs/3_field_types.md#dataclasses)
  * [ Defining custom types](docs/3_field_types.md#defining-custom-types)
### [ Validation](docs/4_validation.md)

  * [ Automatic validation](docs/4_validation.md#automatic-validation)
    * [ Performing post initialisation processing](docs/4_validation.md#performing-post-initialisation-processing)
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
    * [ Nested mapping](docs/6_serialisation.md#nested-mapping)
### [ Detailed schema](docs/7_detailed_schemas.md)
  * [ `gata.Field` properties](docs/7_detailed_schemas.md#gatafield-properties)
    * [ Custom serialisers/deserialisers](docs/7_detailed_schemas.md#custom-serialisersdeserialisers)
