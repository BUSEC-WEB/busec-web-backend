from argparse import ArgumentParser
from typing import Any

from django.core.management import call_command
from django.db import transaction
from django.utils import timezone

from features.accounts.models import User
from features.content.models import Post
from shared.management.base import DevelopmentCommand

SAMPLE_BODIES: dict[str, str] = {
    Post.Type.ARTICLE: "Sample article body.\n\nA second paragraph.",
    Post.Type.POEM: "A sample poem,\n    with its indentation\n\nand stanza breaks kept.",
    Post.Type.LITERATURE: "A sample piece of literature.\n\n  Spacing is preserved.",
}


class Command(DevelopmentCommand):
    help = (
        "Fill the dev database with test users and one post per type and status. "
        "Safe to re-run (DEBUG only)."
    )

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--password", required=True, help="Password for the test users."
        )

    @transaction.atomic
    def handle(self, *args: Any, password: str, **options: Any) -> None:
        call_command("create_test_users", password=password, stdout=self.stdout)
        author = User.objects.get(username="test_journalist")

        created = sum(
            self._seed_post(author, post_type, post_status)
            for post_type in Post.Type
            for post_status in Post.Status
        )
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new post(s)."))

    def _seed_post(self, author: User, post_type: str, post_status: str) -> bool:
        is_published = post_status == Post.Status.PUBLISHED
        _, created = Post.all_objects.get_or_create(  # type: ignore
            title=f"Sample {post_type} ({post_status})",
            defaults={
                "type": post_type,
                "status": post_status,
                "author": author,
                "author_byline": author.username,
                "body": SAMPLE_BODIES[post_type],
                "publish_date": timezone.now() if is_published else None,
            },
        )
        return created
