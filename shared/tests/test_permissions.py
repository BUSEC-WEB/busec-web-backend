from types import SimpleNamespace
from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from features.accounts.factories import (
    ExecutiveFactory,
    JournalistFactory,
    SiteAdminFactory,
)
from features.accounts.models import User
from features.content.factories import PostFactory
from features.content.models import Post
from shared.permissions import (
    IsAuthorOrExecutive,
    IsExecutive,
    IsJournalistOrExecutive,
)

VIEW = APIView()


def request_as(user: Any) -> Request:
    request = Request(APIRequestFactory().get("/"))
    request.user = user
    return request


class RolePermissionTests(TestCase):
    """Who may reach a view, by role (PRD §3)."""

    executive: User
    journalist: User
    site_admin: User

    @classmethod
    def setUpTestData(cls) -> None:
        cls.executive = ExecutiveFactory.create()
        cls.journalist = JournalistFactory.create()
        cls.site_admin = SiteAdminFactory.create()

    def assert_allowed(self, permission: Any, user: Any, expected: bool) -> None:
        self.assertIs(permission.has_permission(request_as(user), VIEW), expected)

    def test_is_executive(self) -> None:
        self.assert_allowed(IsExecutive(), self.executive, True)
        self.assert_allowed(IsExecutive(), self.journalist, False)
        self.assert_allowed(IsExecutive(), self.site_admin, False)
        self.assert_allowed(IsExecutive(), AnonymousUser(), False)

    def test_is_journalist_or_executive(self) -> None:
        self.assert_allowed(IsJournalistOrExecutive(), self.executive, True)
        self.assert_allowed(IsJournalistOrExecutive(), self.journalist, True)
        self.assert_allowed(IsJournalistOrExecutive(), self.site_admin, False)
        self.assert_allowed(IsJournalistOrExecutive(), AnonymousUser(), False)

    def test_is_author_or_executive_admits_editorial_staff_to_the_view(self) -> None:
        self.assert_allowed(IsAuthorOrExecutive(), self.executive, True)
        self.assert_allowed(IsAuthorOrExecutive(), self.journalist, True)
        self.assert_allowed(IsAuthorOrExecutive(), self.site_admin, False)
        self.assert_allowed(IsAuthorOrExecutive(), AnonymousUser(), False)


class IsAuthorOrExecutiveObjectTests(TestCase):
    """Who may act on a specific authored object."""

    author: User
    other_journalist: User
    executive: User
    site_admin: User
    post: Post

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = JournalistFactory.create()
        cls.other_journalist = JournalistFactory.create()
        cls.executive = ExecutiveFactory.create()
        cls.site_admin = SiteAdminFactory.create()
        cls.post = PostFactory.create(author=cls.author)

    def assert_allowed(self, user: Any, obj: Any, expected: bool) -> None:
        permission = IsAuthorOrExecutive()
        self.assertIs(
            permission.has_object_permission(request_as(user), VIEW, obj), expected
        )

    def test_author_may_act_on_own_object(self) -> None:
        self.assert_allowed(self.author, self.post, True)

    def test_other_journalist_may_not(self) -> None:
        self.assert_allowed(self.other_journalist, self.post, False)

    def test_executive_may_act_on_anyones_object(self) -> None:
        self.assert_allowed(self.executive, self.post, True)

    def test_site_admin_may_not(self) -> None:
        self.assert_allowed(self.site_admin, self.post, False)

    def test_anonymous_may_not(self) -> None:
        self.assert_allowed(AnonymousUser(), self.post, False)

    def test_object_without_an_author_is_denied_to_journalists(self) -> None:
        self.assert_allowed(self.author, SimpleNamespace(), False)
