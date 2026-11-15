"""Test data builders for the accounts slice. Each slice keeps its own factories.py."""

from typing import Any

from factory.declarations import LazyAttribute, Sequence
from factory.django import DjangoModelFactory, Password

from features.accounts.models import User

DEFAULT_PASSWORD = "test-password-123"


def _username(n: int) -> str:
    return f"user{n}"


def _email(user: Any) -> str:
    # `user` is factory-boy's resolver for the user being built, not a saved User.
    return f"{user.username}@example.com"


class UserFactory(DjangoModelFactory[User]):
    class Meta:  # type: ignore
        model = User
        django_get_or_create = ("username",)

    username = Sequence(_username)
    email = LazyAttribute(_email)
    password = Password(DEFAULT_PASSWORD)
    role = User.Role.JOURNALIST


class JournalistFactory(UserFactory):
    role = User.Role.JOURNALIST


class ExecutiveFactory(UserFactory):
    role = User.Role.EXECUTIVE


class SiteAdminFactory(UserFactory):
    role = User.Role.SITE_ADMIN
