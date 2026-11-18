"""Sample model tests: behaviour that lives on the model. Copy this pattern."""

import pytest

from features.content.factories import PostFactory
from features.content.models import Post

pytestmark = pytest.mark.django_db


def test_new_post_starts_as_an_unpublished_draft() -> None:
    post = PostFactory.create()

    assert post.status == Post.Status.DRAFT
    assert post.publish_date is None
    assert post.featured is False


def test_poem_body_is_stored_verbatim() -> None:
    body = "First line,\n    indented second\n\nnew stanza"

    post = PostFactory.create(type=Post.Type.POEM, body=body)

    post.refresh_from_db()
    assert post.body == body
