from argparse import ArgumentParser
from typing import Any

from django.db import transaction

from features.accounts.models import User
from shared.management.base import DevelopmentCommand

TEST_USERS: tuple[tuple[str, User.Role], ...] = (
    ("test_executive", User.Role.EXECUTIVE),
    ("test_journalist", User.Role.JOURNALIST),
)


class Command(DevelopmentCommand):
    help = "Create or reset a test executive and a test journalist (DEBUG only)."

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--password", required=True, help="Password set on both accounts."
        )

    @transaction.atomic
    def handle(self, *args: Any, password: str, **options: Any) -> None:
        for username, role in TEST_USERS:
            user, created = User.objects.update_or_create(
                username=username,
                defaults={"role": role, "email": f"{username}@example.com"},
            )
            user.set_password(password)
            user.save(update_fields=["password"])
            action = "Created" if created else "Reset"
            self.stdout.write(self.style.SUCCESS(f"{action} {role}: {username}"))
