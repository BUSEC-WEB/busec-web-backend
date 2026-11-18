"""Sample service tests: business rules in services.py, no HTTP involved.

Copy this pattern for your slice. Model sample: test_models.py.
API permission sample: features/accounts/tests/test_api.py (`test_me_*`).
"""

from collections.abc import Callable

import pytest

from features.content import services
from features.content.factories import PostFactory
from features.content.models import Post
from shared.exceptions import InvalidTransition

pytestmark = pytest.mark.django_db


def test_submit_moves_a_draft_to_review() -> None:
    post = PostFactory.create()

    services.submit(post)

    post.refresh_from_db()
    assert post.status == Post.Status.SUBMITTED


def test_publish_makes_a_submitted_post_public() -> None:
    post = PostFactory.create(status=Post.Status.SUBMITTED)

    services.publish(post)

    post.refresh_from_db()
    assert post.status == Post.Status.PUBLISHED
    assert post.publish_date is not None


def test_send_back_returns_a_submitted_post_to_draft() -> None:
    post = PostFactory.create(status=Post.Status.SUBMITTED)

    services.send_back(post)

    post.refresh_from_db()
    assert post.status == Post.Status.DRAFT


@pytest.mark.parametrize(
    ("start", "step"),
    [
        (Post.Status.DRAFT, services.publish),
        (Post.Status.DRAFT, services.send_back),
        (Post.Status.SUBMITTED, services.submit),
        (Post.Status.PUBLISHED, services.submit),
        (Post.Status.PUBLISHED, services.publish),
        (Post.Status.PUBLISHED, services.send_back),
    ],
)
def test_disallowed_moves_raise_and_change_nothing(
    start: str, step: Callable[[Post], Post]
) -> None:
    post = PostFactory.create(status=start)

    with pytest.raises(InvalidTransition):
        step(post)

    post.refresh_from_db()
    assert post.status == start
