# busec-web-backend

Django + DRF API for the BUSEC blog (see the PRD). Organised as vertical slices: each feature owns everything it needs in `features/<name>/`.

## Setup

```bash
cp .env.example .env        # then fill in your values
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

- Swagger UI: <http://127.0.0.1:8000/api/docs/>
- Admin: <http://127.0.0.1:8000/admin/>
- Health check: <http://127.0.0.1:8000/api/health/>
- Tests: `poetry run python manage.py test`

## Layout

``` text
config/         settings and root urls
shared/env.py   reads and validates .env (add new env keys here)
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
