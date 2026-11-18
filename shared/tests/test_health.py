from unittest import mock

from django.core.cache import cache
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse


class HealthViewTests(TestCase):
    def setUp(self) -> None:
        cache.clear()  # The database check is cached for a few seconds

    def test_healthy(self) -> None:
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"status": "ok", "checks": {"database": "ok"}}
        )

    def test_needs_no_login(self) -> None:
        response = self.client.get(reverse("health"))

        self.assertNotIn(response.status_code, (401, 403))

    def test_database_down_returns_503(self) -> None:
        with mock.patch("shared.views.connection.cursor", side_effect=DatabaseError):
            response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(), {"status": "error", "checks": {"database": "error"}}
        )
