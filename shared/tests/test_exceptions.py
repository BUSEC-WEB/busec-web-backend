from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from django.test import SimpleTestCase
from rest_framework import exceptions
from rest_framework.response import Response

from shared.exceptions import (
    PROBLEM_CONTENT_TYPE,
    InvalidTransition,
    problem_details_exception_handler,
)


def handle(exc: Exception) -> Response:
    response = problem_details_exception_handler(exc, {})
    assert response is not None
    return response


class ProblemDetailsFormatTests(SimpleTestCase):
    """Every handled error comes back in the same shape (RFC 7807)."""

    def assert_problem(
        self,
        response: Response,
        *,
        type_: str,
        status: int,
        errors: Any = None,
    ) -> None:
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.content_type, PROBLEM_CONTENT_TYPE)
        self.assertEqual(set(response.data), {"type", "title", "status", "errors"})
        self.assertEqual(response.data["type"], type_)
        self.assertEqual(response.data["status"], status)
        self.assertIsInstance(response.data["title"], str)
        self.assertEqual(response.data["errors"], errors or {})

    def test_field_validation_errors(self) -> None:
        response = handle(exceptions.ValidationError({"title": ["Required."]}))

        self.assert_problem(
            response,
            type_="validation_error",
            status=400,
            errors={"title": ["Required."]},
        )
        self.assertEqual(response.data["title"], "Invalid input.")

    def test_non_field_validation_errors(self) -> None:
        response = handle(exceptions.ValidationError("Dates overlap."))

        self.assert_problem(
            response,
            type_="validation_error",
            status=400,
            errors={"non_field_errors": ["Dates overlap."]},
        )

    def test_not_authenticated(self) -> None:
        response = handle(exceptions.NotAuthenticated())

        self.assert_problem(response, type_="not_authenticated", status=401)
        self.assertEqual(
            response.data["title"], "Authentication credentials were not provided."
        )

    def test_drf_permission_denied(self) -> None:
        response = handle(exceptions.PermissionDenied())

        self.assert_problem(response, type_="permission_denied", status=403)

    def test_django_permission_denied(self) -> None:
        response = handle(DjangoPermissionDenied())

        self.assert_problem(response, type_="permission_denied", status=403)

    def test_django_404(self) -> None:
        response = handle(Http404())

        self.assert_problem(response, type_="not_found", status=404)

    def test_throttled_keeps_retry_after_header(self) -> None:
        response = handle(exceptions.Throttled(wait=30))

        self.assert_problem(response, type_="throttled", status=429)
        self.assertEqual(response["Retry-After"], "30")

    def test_code_given_at_raise_time_wins_over_the_class_default(self) -> None:
        exc = exceptions.AuthenticationFailed("No account.", code="no_active_account")

        response = handle(exc)

        self.assert_problem(response, type_="no_active_account", status=401)

    def test_nested_detail_is_flattened_into_the_title(self) -> None:
        # simplejwt raises errors whose detail is a dict.
        exc = exceptions.AuthenticationFailed(
            {"detail": "Token is invalid", "code": "token_not_valid"}
        )

        response = handle(exc)

        self.assert_problem(response, type_="authentication_failed", status=401)
        self.assertEqual(response.data["title"], "Token is invalid")


class InvalidTransitionTests(SimpleTestCase):
    def test_maps_to_409_conflict(self) -> None:
        response = handle(InvalidTransition("published", "submitted"))

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content_type, PROBLEM_CONTENT_TYPE)
        self.assertEqual(
            response.data,
            {
                "type": "invalid_transition",
                "title": "Cannot move from 'published' to 'submitted'.",
                "status": 409,
                "errors": {},
            },
        )

    def test_keeps_the_states_for_callers(self) -> None:
        exc = InvalidTransition("draft", "published")

        self.assertEqual((exc.current, exc.target), ("draft", "published"))

    def test_subclasses_are_handled_too(self) -> None:
        class PostTransitionError(InvalidTransition):
            pass

        response = handle(PostTransitionError("draft", "published"))

        self.assertEqual(response.status_code, 409)


class UnhandledExceptionTests(SimpleTestCase):
    def test_unexpected_errors_are_left_to_django(self) -> None:
        self.assertIsNone(problem_details_exception_handler(ValueError("boom"), {}))
