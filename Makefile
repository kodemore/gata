.DEFAULT_GOAL := all

isort:
	poetry run isort -c setup.cfg

black:
	poetry run black --line-length=120 --target-version py38 gata

mypy:
	poetry run mypy gata

test:
	poetry run pytest

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

publish:
	poetry publish --build
