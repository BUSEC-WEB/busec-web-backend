from io import StringIO

from django.contrib.auth import authenticate
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from features.accounts.models import User

PASSWORD = "correct-horse-battery"


@override_settings(DEBUG=True)
class CreateTestUsersCommandTests(TestCase):
    def run_command(self, password: str = PASSWORD) -> str:
        out = StringIO()
        call_command("create_test_users", password=password, stdout=out)
        return out.getvalue()

    def test_creates_an_executive_and_a_journalist(self) -> None:
        self.run_command()

        self.assertEqual(
            User.objects.get(username="test_executive").role, User.Role.EXECUTIVE
        )
        self.assertEqual(
            User.objects.get(username="test_journalist").role, User.Role.JOURNALIST
        )

    def test_users_can_sign_in_with_the_given_password(self) -> None:
        self.run_command()

        for username in ("test_executive", "test_journalist"):
            self.assertIsNotNone(authenticate(username=username, password=PASSWORD))

    def test_rerunning_resets_password_and_role_without_duplicates(self) -> None:
        self.run_command()
        User.objects.filter(username="test_executive").update(role=User.Role.JOURNALIST)

        output = self.run_command(password="a-new-password")

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            User.objects.get(username="test_executive").role, User.Role.EXECUTIVE
        )
        self.assertIsNotNone(
            authenticate(username="test_journalist", password="a-new-password")
        )
        self.assertIn("Reset", output)

    @override_settings(DEBUG=False)
    def test_refuses_to_run_without_debug(self) -> None:
        with self.assertRaisesMessage(CommandError, "DEBUG=true"):
            self.run_command()

        self.assertFalse(User.objects.exists())
