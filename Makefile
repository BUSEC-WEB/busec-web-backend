.PHONY: run test coverage lint migrate seed

run:
	poetry run python manage.py runserver

# Runs every test (pytest style and Django TestCase); settings come from pyproject.toml.
test:
	poetry run pytest

coverage:
	poetry run coverage run -m pytest
	poetry run coverage report

# NOTE: run this command before pushing any code.
lint:
	poetry run ruff check --fix .
	poetry run ruff format .
	poetry run mypy .

migrate:
	poetry run python manage.py migrate

# Dev only - Usage: make seed PASSWORD=<test users' password>
seed:
	poetry run python manage.py seed --password "$(PASSWORD)"
