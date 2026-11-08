## Description

<!-- What does this PR do and why? -->

## Related PRD section / issues

<!-- e.g. PRD §5.3 E-magazine. Use "Closes #123" to auto-close an issue. -->

## Type of change

- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring (no functional changes)
- [ ] Documentation update
- [ ] Infrastructure / CI/CD
- [ ] Performance improvement

## Changes made

<!-- List the specific changes. Be precise. -->

-

## API, data and config impact

- [ ] Endpoints added or changed (describe below, with request/response examples)
- [ ] Breaking change for API consumers
- [ ] Models changed and migrations added (no merged migrations edited)
- [ ] Permissions or role behaviour changed (journalist, executive, site_admin)
- [ ] Environment variables added or changed (updated `shared/env.py` and `.env.example`)
- [ ] Dependencies changed (`pyproject.toml` / `poetry.lock`, approved beforehand)
- [ ] None of the above

<!-- Details, request/response examples, rollout or backfill notes: -->

## How to test

<!-- Steps for reviewers to verify this works (e.g. endpoint in /api/docs/). -->

1.

## Checklist

- [ ] Branch is not `main` nor `development`, and only the files and folders for this task were touched
- [ ] `poetry run ruff check .` passes
- [ ] `poetry run ruff format --check .` passes
- [ ] `poetry run mypy .` passes
- [ ] `poetry run python manage.py makemigrations --check --dry-run` reports no changes
- [ ] Tests added or updated where applicable, and `coverage` meets the 85% threshold
- [ ] OpenAPI schema / Swagger still renders correctly
- [ ] Documentation updated if needed (README, PRD references)
- [ ] No secrets or `.env` committed, and no new warnings introduced
