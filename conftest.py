"""Project-wide pytest fixtures. Slice-specific fixtures go in that slice's conftest.py."""

from collections.abc import Callable

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from features.accounts.factories import ExecutiveFactory, JournalistFactory
from features.accounts.models import User


@pytest.fixture
def api_client() -> APIClient:
    """An anonymous client, as a reader would be."""
    return APIClient()


@pytest.fixture
def journalist(db: None) -> User:
    return JournalistFactory.create()


@pytest.fixture
def executive(db: None) -> User:
    return ExecutiveFactory.create()


@pytest.fixture
def auth_client() -> Callable[[User], APIClient]:
    """Returns a client signed in as the given user, with a real JWT.

    Usage: `auth_client(executive).post(url, data)`.
    """

    def signed_in_as(user: User) -> APIClient:
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(user)}")
        return client

    return signed_in_as
