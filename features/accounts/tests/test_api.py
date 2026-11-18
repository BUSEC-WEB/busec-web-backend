from collections.abc import Callable
from typing import Any

import pytest
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from features.accounts.models import User
from shared.exceptions import PROBLEM_CONTENT_TYPE

PASSWORD = "correct-horse-battery"

LOGIN_URL = reverse("accounts:login")
REFRESH_URL = reverse("accounts:refresh")
LOGOUT_URL = reverse("accounts:logout")
ME_URL = reverse("accounts:me")


class AuthTestCase(APITestCase):
    user: User

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="journalist",
            password=PASSWORD,
            email="journalist@example.com",
            role=User.Role.JOURNALIST,
        )

    def login(self, username: str = "journalist", password: str = PASSWORD) -> Response:
        return self.client.post(
            LOGIN_URL, {"username": username, "password": password}, format="json"
        )

    def tokens(self) -> dict[str, str]:
        response = self.login()
        self.assertEqual(response.status_code, 200)
        return dict(response.data)

    def refresh(self, refresh_token: str) -> Response:
        return self.client.post(REFRESH_URL, {"refresh": refresh_token}, format="json")

    def assert_problem(self, response: Any, status: int, type_: str) -> None:
        self.assertEqual(response.status_code, status)
        self.assertEqual(response["Content-Type"], PROBLEM_CONTENT_TYPE)
        self.assertEqual(response.json()["type"], type_)


class LoginTests(AuthTestCase):
    def test_valid_credentials_return_a_token_pair(self) -> None:
        response = self.login()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {"access", "refresh"})

    def test_wrong_password_is_rejected(self) -> None:
        response = self.login(password="wrong")

        self.assert_problem(response, 401, "no_active_account")

    def test_unknown_user_is_rejected(self) -> None:
        response = self.login(username="nobody")

        self.assert_problem(response, 401, "no_active_account")

    def test_inactive_user_is_rejected(self) -> None:
        self.user.is_active = False
        self.user.save()

        response = self.login()

        self.assert_problem(response, 401, "no_active_account")

    def test_missing_fields_are_reported_per_field(self) -> None:
        response = self.client.post(LOGIN_URL, {}, format="json")

        self.assert_problem(response, 400, "validation_error")
        self.assertEqual(set(response.json()["errors"]), {"username", "password"})


class MeTests(AuthTestCase):
    def test_returns_the_signed_in_user(self) -> None:
        access = self.tokens()["access"]

        response = self.client.get(ME_URL, HTTP_AUTHORIZATION=f"Bearer {access}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "id": self.user.pk,
                "username": "journalist",
                "email": "journalist@example.com",
                "first_name": "",
                "last_name": "",
                "role": User.Role.JOURNALIST,
            },
        )

    def test_never_exposes_the_password(self) -> None:
        access = self.tokens()["access"]

        response = self.client.get(ME_URL, HTTP_AUTHORIZATION=f"Bearer {access}")

        self.assertNotIn("password", response.data)

    def test_requires_authentication(self) -> None:
        response = self.client.get(ME_URL)

        self.assert_problem(response, 401, "not_authenticated")

    def test_rejects_an_invalid_token(self) -> None:
        response = self.client.get(ME_URL, HTTP_AUTHORIZATION="Bearer not-a-token")

        self.assert_problem(response, 401, "token_not_valid")

    def test_rejects_a_refresh_token_used_as_access(self) -> None:
        refresh = self.tokens()["refresh"]

        response = self.client.get(ME_URL, HTTP_AUTHORIZATION=f"Bearer {refresh}")

        self.assert_problem(response, 401, "token_not_valid")

    def test_is_read_only(self) -> None:
        access = self.tokens()["access"]

        response = self.client.patch(
            ME_URL,
            {"role": User.Role.EXECUTIVE},
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )

        self.assert_problem(response, 405, "method_not_allowed")
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, User.Role.JOURNALIST)


class RefreshTests(AuthTestCase):
    def test_returns_a_new_pair(self) -> None:
        refresh = self.tokens()["refresh"]

        response = self.refresh(refresh)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {"access", "refresh"})
        self.assertNotEqual(response.data["refresh"], refresh)

    def test_a_rotated_refresh_token_cannot_be_reused(self) -> None:
        refresh = self.tokens()["refresh"]
        self.refresh(refresh)

        response = self.refresh(refresh)

        self.assert_problem(response, 401, "token_not_valid")

    def test_rejects_garbage(self) -> None:
        response = self.refresh("not-a-token")

        self.assert_problem(response, 401, "token_not_valid")


class LogoutTests(AuthTestCase):
    def test_revokes_the_refresh_token(self) -> None:
        refresh = self.tokens()["refresh"]

        logout = self.client.post(LOGOUT_URL, {"refresh": refresh}, format="json")
        response = self.refresh(refresh)

        self.assertEqual(logout.status_code, 200)
        self.assert_problem(response, 401, "token_not_valid")


# API permission sample (pytest style): copy this pattern for slice endpoints.
# Fixtures come from the root conftest.py.


def test_me_rejects_anonymous_readers(api_client: APIClient) -> None:
    response = api_client.get(ME_URL)

    assert response.status_code == 401


@pytest.mark.parametrize("role", ["journalist", "executive"])
def test_me_is_open_to_staff(
    role: str,
    request: pytest.FixtureRequest,
    auth_client: Callable[[User], APIClient],
) -> None:
    user: User = request.getfixturevalue(role)

    response = auth_client(user).get(ME_URL)

    assert response.status_code == 200
    assert response.data["role"] == role
