# Architecture decisions

Short records of decisions that shape the backend. Each one says what we chose, why, and what it means for day-to-day work. To change a decision, add a new entry that supersedes the old one rather than rewriting history.

ADR - Alternative Dispute Resolution.

## ADR-001: Django + Django REST Framework

**Status:** Accepted

**Context.** A staff workflow that needs login, roles and an admin panel (PRD §3, §4.1). PRD §7 weighed Django against FastAPI.

**Decision.** Django with Django REST Framework, PostgreSQL, and drf-spectacular for the OpenAPI schema (`/api/schema/`, `/api/docs/`).

**Consequences.**

- Auth, permissions, the admin panel, migrations and the ORM come built in, so time goes into BUSEC features instead.
- The React frontend talks to the API only. Django serves no pages except the admin.
- We follow Django conventions (apps, settings, management commands) rather than inventing our own.

## ADR-002: One slice per Django app, no cross-slice imports

**Status:** Accepted

**Context.** Several people work on separate features at once. Shared code that every feature reaches into causes merge conflicts and hidden coupling.

**Decision.** Each feature is a vertical slice and a Django app in `features/<slice>/` (`accounts`, `content`, `magazine`, `committee`, `newsletter`). A slice may import only from:

- itself,
- `shared/` (the core: base models, permissions, pagination, errors, settings helpers),
- `features/accounts` (users and roles are needed everywhere).

**Consequences.**

- Each slice owns its models, migrations, routes (mounted at `/api/v1/<slice>/`) and tests, so slice owners never edit root config.
- If two slices need the same thing, it moves to `shared/` instead of one slice importing the other.
- `shared/` application code imports only `accounts`. Tests in `shared/tests/` use `content.Post` as a concrete model for the abstract base models; this is the one allowed exception.
- See [Slice folder convention](../README.md#slice-folder-convention) for the files inside a slice.

## ADR-003: Status changes only through action endpoints

**Status:** Accepted

**Context.** Posts move through draft → submitted → published, or are sent back to draft (PRD §5.2). If `status` were a writable field, any update could skip review or publish without an executive.

**Decision.** `status` is read-only on every serializer. Each transition is its own action endpoint (for example `POST /api/v1/content/posts/{id}/submit/`, `publish/`, `send-back/`) that calls a function in the slice's `services.py`.

**Consequences.**

- The allowed moves live in one place (`features/content/services.py`). A refused move raises `InvalidTransition` and returns `409 Conflict`.
- Each action carries its own permission: journalists submit, only executives publish or send back.
- The same pattern applies to any future state machine in another slice.

## ADR-004: Journalists edit only their own drafts, executives edit anything

**Status:** Accepted as the default; not totally finalised (PRD §3 and §14, open question 4).

**Context.** The PRD recommends this default but leaves it open.

**Decision.**

- A journalist may edit a post only if they are its author and it is a draft.
- An executive may edit any post in any status.
- Site admins manage accounts through the Django admin and have no content rights.

**Consequences.**

- Views combine `shared.permissions.IsAuthorOrExecutive` (author or executive) with a draft-only check for journalists.
- Once a journalist submits a post, it is locked for them until an executive sends it back.
- If the committee chooses otherwise, only the permission check changes. The API shape stays the same.

## ADR-005: Soft delete for posts

**Status:** Accepted

**Context.** Only executives may delete, and mistakes must be recoverable (PRD §5.2).

**Decision.** `Post` inherits `shared.models.SoftDeleteModel`. Deleting sets `deleted_at` instead of removing the row.

**Consequences.**

- `Post.objects` hides deleted posts everywhere, including public endpoints and related lookups. `Post.all_objects` sees everything, for restore and admin views.
- The API delete endpoint is executive-only and calls `soft_delete()`. Restoring calls `restore()`.
- Rows are never removed through the API. Permanent removal, if ever needed, is a deliberate admin or database task.

## ADR-006: JWT authentication

**Status:** Accepted

**Context.** The React app is hosted separately from the API (PRD §7, §9), so cookie sessions across domains would add CSRF and cookie-domain setup. Readers never sign in; only staff do.

**Decision.** JSON Web Tokens with `djangorestframework-simplejwt`, sent as `Authorization: Bearer <access>`.

- Endpoints: `POST /api/v1/accounts/login/`, `refresh/`, `logout/`, and `GET /api/v1/accounts/me/`.
- Access tokens last 15 minutes and refresh tokens 7 days.
- Refresh tokens rotate on every refresh, and the old one is blacklisted. Logout blacklists the current refresh token.

**Consequences.**

- Every endpoint requires a signed-in user by default. Public reader endpoints opt out with `permission_classes = [AllowAny]`.
- A stolen access token works for at most 15 minutes. A refresh token is useless after logout or rotation.
- The frontend refreshes the access token before it expires and calls `me/` to tailor the UI to the user's role.
