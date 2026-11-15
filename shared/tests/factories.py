"""Small builders shared by the test modules (plain ORM, no extra dependencies)."""

from features.accounts.models import User
from features.content.models import Post


def make_user(username: str, role: str = User.Role.JOURNALIST) -> User:
    return User.objects.create_user(username=username, password="unused", role=role)


def make_post(author: User, title: str = "A post") -> Post:
    return Post.objects.create(
        type=Post.Type.ARTICLE,
        title=title,
        author_byline=author.username,
        body="Body.",
        author=author,
    )  # pyright: ignore[reportUnknownVariableType]
