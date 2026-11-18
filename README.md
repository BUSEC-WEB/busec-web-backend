# busec-web-backend

Django + DRF API for the BUSEC blog (see the PRD). Organised as vertical slices: each feature owns everything it needs in `features/<name>/`.

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- PostgreSQL (connection string set in `.env`)

## Setup

Needs PostgreSQL running and its URL in `.env`.

```bash
cp .env.example .env               # then fill in your values
poetry install                     # runtime and dev dependencies
make migrate                       # create the database tables
make seed PASSWORD=<pick-one>      # dev data: test_executive, test_journalist, sample posts
make run                           # API on http://127.0.0.1:8000
```

- Swagger UI: <http://127.0.0.1:8000/api/docs/> (click **Authorize** and paste an access token from `POST /api/v1/accounts/login/`)
- Admin: <http://127.0.0.1:8000/admin/> (create an account with `poetry run python manage.py createsuperuser`)
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
| `SECURE_MODE` | `true` in production: HTTPS redirect, secure cookies, HSTS (default `false`) |
| `S3_ENDPOINT` | S3-compatible storage host and port, no scheme (MinIO in dev, e.g. `localhost:9000`) |
| `S3_SECURE` | `true` to connect over HTTPS (default `true`) |
| `S3_ACCESS_KEY` / `S3_SECRET_KEY` | Storage credentials |
| `S3_MAGAZINE_BUCKET` | Bucket for e-magazine PDFs |
| `S3_COVER_IMAGE_BUCKET` | Bucket for cover images |

Uploads go to these buckets through django-storages; the buckets must already exist. A model field picks a bucket by its `STORAGES` alias with `shared.storage.StorageAlias("magazine_pdfs")`. File URLs are signed and expire after an hour.

Never commit `.env`.

## Tests and checks

```bash
make test        # every test, with pytest
make coverage    # tests plus coverage report (fails under 70%)
make lint        # ruff fix + format, then mypy; run before pushing
poetry run python manage.py makemigrations --check --dry-run   # no missing migrations
```

CI (`.github/workflows/ci.yml`) runs ruff, mypy, the migrations check and the tests with coverage on pushes and pull requests to `development` and `dev-onuchukwu`.

Tests use pytest. Shared fixtures live in the root `conftest.py`: `api_client`, `journalist`, `executive`, and `auth_client(user)` (a client signed in with a real JWT). Each slice builds test data with factory-boy factories in its `factories.py`.

Migrations are excluded from ruff formatting and from the `RUF012` rule. Don't edit merged migrations.

## Layout

``` text
config/           settings and root urls
conftest.py       pytest fixtures shared by every slice
docs/
  decisions.md    architecture decisions (ADRs)
shared/           core building blocks, used by every slice
  env.py          reads and validates .env (add new env keys here)
  models.py       TimeStampedModel, SoftDeleteModel
  permissions.py  IsExecutive, IsJournalistOrExecutive, IsAuthorOrExecutive
  exceptions.py   one error format; InvalidTransition (409)
  pagination.py   StandardPagination
  views.py        health check (database check, cached for 5 seconds)
  management/     DevelopmentCommand base (DEBUG-only commands)
features/
  accounts/       staff users, roles, JWT auth
  content/        articles, poems, literature, editorial workflow
  magazine/       e-magazine issues
  committee/      committee members by tenure year
  newsletter/     subscriber signup
```

The reasons behind the structure are in [docs/decisions.md](docs/decisions.md).

## Slice folder convention

Every slice in `features/<slice>/` uses the same files. Create a file when you need it.

``` text
features/<slice>/
  models.py        data, plus behaviour that belongs to a single row
  services.py      business rules and state changes (e.g. submit, publish); no HTTP
  serializers.py   request validation and response shape; status fields are read-only
  views.py         thin: permissions, call a service, return a response
  permissions.py   rules specific to this slice, built on shared/permissions.py
  urls.py          the slice's router, mounted at /api/v1/<slice>/
  factories.py     factory-boy test data builders
  management/      slice-owned management commands
  migrations/
  tests/
    test_models.py
    test_services.py
    test_api.py    endpoints and permissions
```

A slice imports only from itself, `shared/` and `features/accounts` (see ADR-002). The PRD requirements for a slice are listed at the top of its `models.py`.

## Working on a slice

1. Write the model in `models.py`, then run `poetry run python manage.py makemigrations <slice>` and `make migrate`.
2. Put business rules in `services.py`. Change statuses only there, through action endpoints (ADR-003).
3. Write the serializer, then the view (`viewsets.ModelViewSet` covers CRUD).
4. Register viewsets on the `router` in the slice's `urls.py`. It's already mounted at `/api/v1/<slice>/`.
5. Add tests in `features/<slice>/tests/`. Copy the samples: `features/content/tests/test_models.py`, `test_services.py`, and the `test_me_*` tests in `features/accounts/tests/test_api.py`. Then check the endpoint in Swagger.

Defaults already set in `config/settings.py`: JWT auth, every endpoint requires login unless the view sets `permission_classes = [AllowAny]` (public reader endpoints), pagination (`shared.pagination.StandardPagination`, 20 per page, `?page_size=` up to 100), filtering with `filterset_fields`, CORS origins from `.env`, and a `newsletter` throttle rate (use `throttle_scope = "newsletter"`).

Errors all use one format: `{"type", "title", "status", "errors"}` (`application/problem+json`). Raise `InvalidTransition(current, target)` for a refused status change (returns 409).

Auth (`/api/v1/accounts/`): `login/`, `refresh/`, `logout/` (blacklists the refresh token), `me/`. Send `Authorization: Bearer <access>`.
