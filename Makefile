.DEFAULT_GOAL := all

isort:
	poetry run isort -c setup.cfg

black:
	poetry run black --line-length=120 --target-version py38 gata

mypy:
	poetry run mypy gata

test:
	poetry run pytest

test-codecov:
	poetry run pytest --ignore venv -W ignore::DeprecationWarning --cov=gata --cov-report=term-missing
	poetry run codecov

lint:
	poetry run isort -c setup.cfg
	poetry run black --line-length=120 --target-version py38 gata
	poetry run mypy gata

all:
	poetry run isort -c setup.cfg
	poetry run black --line-length=120 --target-version py38 gata
	poetry run mypy gata
	poetry run pytest

build:
	poetry run isort -c setup.cfg
	poetry run black --line-length=120 --target-version py38 gata
	poetry run mypy gata
	poetry run pytest
	poetry build

docs:
	poetry run docs/build_docs.py

publish:
	poetry publish --build
