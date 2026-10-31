# busec-web-backend

Django + DRF backend organised as vertical slices: each feature lives in `features/<name>/` with its own views, serializers, storage, urls and tests.

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver   # Swagger UI: http://127.0.0.1:8000/api/docs/
poetry run python manage.py test
```

New slice: copy `features/todos/`, add it to `INSTALLED_APPS`, and include its urls in `config/urls.py`.
