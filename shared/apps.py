from django.apps import AppConfig


class SharedConfig(AppConfig):
    """Cross-cutting building blocks used by every feature slice."""

    name = "shared"
