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
- [ ] `make lint` passes (ruff check, ruff format, mypy)
- [ ] Tests added or updated in `features/<slice>/tests/`, and `make coverage` passes (70% threshold)
- [ ] Migrations included for every model change, and `poetry run python manage.py makemigrations --check --dry-run` reports no changes
- [ ] API schema still valid: `poetry run python manage.py spectacular --validate --fail-on-warn --file /dev/null` passes and `/api/docs/` renders
- [ ] Docs updated if needed (README, `docs/decisions.md` for a new or changed decision)
- [ ] Slice rules kept: imports only from the slice itself, `shared/` and `features/accounts`; status changes only via action endpoints
- [ ] No secrets or `.env` committed, and no new warnings introduced
