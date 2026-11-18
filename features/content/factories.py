"""Test data builders for the content slice."""

from typing import Any

from factory.declarations import LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory

from features.accounts.factories import JournalistFactory
from features.content.models import Post


def _title(n: int) -> str:
    return f"Post {n}"


def _byline(post: Any) -> str:
    # `post` is factory-boy's resolver for the post being built.
    return str(post.author.username)


class PostFactory(DjangoModelFactory[Post]):
    class Meta:  # type: ignore
        model = Post

    type = Post.Type.ARTICLE
    title = Sequence(_title)
    author = SubFactory(JournalistFactory)
    author_byline = LazyAttribute(_byline)
    body = "Body."
    status = Post.Status.DRAFT
