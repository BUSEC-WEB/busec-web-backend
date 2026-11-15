"""One error format for the whole API: RFC 7807 problem details.

    {"type": "<code>", "title": "<message>", "status": <http status>, "errors": {...}}

`errors` carries per-field messages for validation failures and is empty otherwise.
Unhandled exceptions are left to Django so they are logged and reported as 500s.
"""

from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

PROBLEM_CONTENT_TYPE = "application/problem+json"


class InvalidTransition(Exception):
    """A state machine refused a move, e.g. publishing a draft that was never
    submitted. Slices raise this (or a subclass) from their domain code; the API
    answers with 409 Conflict."""

    def __init__(self, current: str, target: str) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Cannot move from {current!r} to {target!r}.")


class _Conflict(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "invalid_transition"


def problem_details_exception_handler(
    exc: Exception, context: dict[str, Any]
) -> Response | None:
    api_exception = _as_api_exception(exc)
    if api_exception is None:
        return None

    # DRF's handler adds auth/throttle headers and rolls back atomic requests.
    response = drf_exception_handler(api_exception, context)
    if response is None:
        return None

    response.data = _problem(api_exception, response.status_code)
    response.content_type = PROBLEM_CONTENT_TYPE
    return response


def _as_api_exception(exc: Exception) -> exceptions.APIException | None:
    if isinstance(exc, exceptions.APIException):
        return exc
    if isinstance(exc, InvalidTransition):
        return _Conflict(str(exc))
    if isinstance(exc, Http404):
        return exceptions.NotFound()
    if isinstance(exc, PermissionDenied):
        return exceptions.PermissionDenied()
    return None


def _problem(exc: exceptions.APIException, status_code: int) -> dict[str, Any]:
    if isinstance(exc, exceptions.ValidationError):
        return {
            "type": "validation_error",
            "title": "Invalid input.",
            "status": status_code,
            "errors": _field_errors(exc.detail),
        }
    return {
        "type": _code(exc),
        "title": _message(exc.detail),
        "status": status_code,
        "errors": {},
    }


def _code(exc: exceptions.APIException) -> str:
    """Prioritize the specific error code from the raise call (e.g., "no_active_account")
    over the default exception code ("authentication_failed")."""
    codes = exc.get_codes()
    return codes if isinstance(codes, str) else exc.default_code


def _field_errors(detail: Any) -> dict[str, Any]:
    return detail if isinstance(detail, dict) else {"non_field_errors": detail}  # type: ignore


def _message(detail: Any) -> str:
    if isinstance(detail, dict):
        return str(detail.get("detail", ""))  # type: ignore
    return str(detail)
