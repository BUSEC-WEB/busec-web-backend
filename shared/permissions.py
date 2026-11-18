"""Role-based access rules (PRD §3), enforced on the backend (PRD §6).
Site admins manage accounts through the Django admin and hold no content rights.
"""

from typing import Any, ClassVar, Protocol, runtime_checkable

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from features.accounts.models import User


@runtime_checkable
class Authored(Protocol):
    """Any object owned by a user through an `author` foreign key."""

    author_id: int


class HasRole(BasePermission):
    """Allows authenticated users whose role is in `allowed_roles`."""

    allowed_roles: ClassVar[frozenset[str]] = frozenset()

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user  # type: ignore
        return isinstance(user, User) and user.role in self.allowed_roles


class IsExecutive(HasRole):
    """Publish, delete, feature content, manage the committee page."""

    allowed_roles = frozenset({User.Role.EXECUTIVE})


class IsJournalistOrExecutive(HasRole):
    """Editorial staff: executives can do everything a journalist can."""

    allowed_roles = frozenset({User.Role.JOURNALIST, User.Role.EXECUTIVE})


class IsAuthorOrExecutive(IsJournalistOrExecutive):
    """Editorial staff may reach the view; only the object's author or an
    executive may act on a given object."""

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        user = request.user  # type: ignore
        if not isinstance(user, User):
            return False
        if user.role == User.Role.EXECUTIVE:
            return True
        return isinstance(obj, Authored) and obj.author_id == user.pk
