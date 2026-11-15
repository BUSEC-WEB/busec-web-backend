"""Editorial workflow for posts (PRD §5.2).

    draft --submit--> submitted --publish--> published
                          |
                          +--send_back--> draft

Views call these functions instead of writing `status` directly, so the rules
live in one place. Who may call each step is enforced by the view's permission
classes (publishing is executive-only); these functions enforce *when*.
"""

from django.utils import timezone

from features.content.models import Post
from shared.exceptions import InvalidTransition

ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    Post.Status.DRAFT: frozenset({Post.Status.SUBMITTED}),
    Post.Status.SUBMITTED: frozenset({Post.Status.PUBLISHED, Post.Status.DRAFT}),
    Post.Status.PUBLISHED: frozenset(),
}


def submit(post: Post) -> Post:
    """A journalist hands a draft over for review."""
    return _move(post, Post.Status.SUBMITTED)


def publish(post: Post) -> Post:
    """An executive makes a submitted post public."""
    post.publish_date = post.publish_date or timezone.now()
    return _move(post, Post.Status.PUBLISHED, "publish_date")


def send_back(post: Post) -> Post:
    """An executive returns a submitted post to its author as a draft."""
    return _move(post, Post.Status.DRAFT)


def _move(post: Post, target: str, *also_save: str) -> Post:
    if target not in ALLOWED_TRANSITIONS[post.status]:
        raise InvalidTransition(post.status, target)  # type: ignore
    post.status = target
    post.save(update_fields=["status", *also_save])
    return post
