# busec-web-backend

Django + DRF API for the BUSEC blog (see the PRD). Organised as vertical slices: each feature owns everything it needs in `features/<name>/`.

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- PostgreSQL (connection string set in `.env`)

## Setup

```bash
cp .env.example .env        # then fill in your values
poetry install              # installs runtime and dev dependencies
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

- Swagger UI: <http://127.0.0.1:8000/api/docs/>
- Admin: <http://127.0.0.1:8000/admin/>
- Health check: <http://127.0.0.1:8000/api/health/> (for uptime monitoring; returns 503 if the database is down)
- API schema: <http://127.0.0.1:8000/api/schema/>

## Environment variables

Read and validated in `shared/env.py` (the app fails at startup if one is invalid). See `.env.example`.

| Variable | Purpose |
| --- | --- |
| `DATABASE_CONNECTION_STRING` | PostgreSQL connection URL |
| `DEBUG` | Django debug mode |
| `SECRET_KEY` | Django secret key |
| `ALLOWED_HOSTS` | Allowed host names |
| `CORS_ALLOWED_ORIGINS` | Origins allowed by CORS |

Never commit `.env`.

## Checks

CI (`.github/workflows/ci.yml`) runs these on pushes and pull requests to `development`, `main` and `dev-onuchukwu`. Run them locally before pushing:

```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy .                                    # django-stubs plugin, settings: config.settings
poetry run python manage.py makemigrations --check --dry-run
poetry run coverage run manage.py test && poetry run coverage report   # fails under 85%
```

Migrations are excluded from ruff formatting and from the `RUF012` rule. Don't edit merged migrations.

## Layout

``` text
config/         settings and root urls
shared/
  env.py        reads and validates .env (add new env keys here)
  views.py      health check view (database check, cached for 5 seconds)
  serializers.py
features/
  accounts/     staff users and roles (journalist, executive, site_admin)
  content/      articles, poems, literature
  magazine/     e-magazine issues
  committee/    committee members by tenure year
  newsletter/   subscriber signup
```

Each slice has `models.py`, `serializers.py`, `views.py` and `urls.py`. The PRD requirements for a slice are listed at the top of its `models.py`.

## Working on a slice

1. Write the model in `models.py`, then run `makemigrations <slice>` and `migrate`.
2. Write the serializer, then the view (`viewsets.ModelViewSet` covers CRUD).
3. Register routes in the slice's `urls.py`. It's already mounted at `/api/<slice>/`.
4. Add tests in `features/<slice>/tests.py` and check the endpoint in Swagger.

Defaults already set in `config/settings.py`: pagination (20 per page), filtering with `filterset_fields`, CORS origins from `.env`, and a `newsletter` throttle rate (use `throttle_scope = "newsletter"`).
