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


## Example
```python
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

[Introduction](docs/1.%20Introduction.md)
