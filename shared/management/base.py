from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class DevelopmentCommand(BaseCommand):
    """Base for commands that create fake accounts or data.
    Refuses to run unless DEBUG is on, so it can never touch production.
    """

    def execute(self, *args: Any, **options: Any) -> str | None:
        if not settings.DEBUG:
            raise CommandError("This command only runs with DEBUG=true.")
        return super().execute(*args, **options)
