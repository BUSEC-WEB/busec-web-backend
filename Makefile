.PHONY: run test coverage pytest lint migrate

run:
	poetry run python manage.py runserver

# no tests exist yet.
test:
	poetry run python manage.py test

coverage:
	poetry run coverage run manage.py test
	poetry run coverage report

pytest:
	poetry run pytest --ds=config.settings

# NOTE: run this command before pushing any code.
lint:
	poetry run ruff check --fix .
	poetry run ruff format .
	poetry run mypy .

migrate:
	poetry run python manage.py migrate
