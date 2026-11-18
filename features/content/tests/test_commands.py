from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from features.content.models import Post

PASSWORD = "seed-password-123"


def seed() -> str:
    out = StringIO()
    call_command("seed", password=PASSWORD, stdout=out)
    return out.getvalue()


@override_settings(DEBUG=True)
class SeedCommandTests(TestCase):
    def test_creates_one_post_per_type_and_status(self) -> None:
        seed()

        self.assertEqual(Post.objects.count(), len(Post.Type) * len(Post.Status))
        for post_type in Post.Type:
            for post_status in Post.Status:
                self.assertTrue(
                    Post.objects.filter(type=post_type, status=post_status).exists()
                )

    def test_only_published_posts_have_a_publish_date(self) -> None:
        seed()

        self.assertFalse(
            Post.objects.filter(
                status=Post.Status.PUBLISHED, publish_date__isnull=True
            ).exists()
        )
        self.assertFalse(
            Post.objects.exclude(status=Post.Status.PUBLISHED)
            .filter(publish_date__isnull=False)
            .exists()
        )

    def test_is_safe_to_run_twice(self) -> None:
        seed()
        output = seed()

        self.assertEqual(Post.objects.count(), len(Post.Type) * len(Post.Status))
        self.assertIn("Seeded 0 new post(s).", output)

    def test_does_not_recreate_soft_deleted_posts(self) -> None:
        seed()
        post = Post.objects.first()
        assert post is not None
        post.soft_delete()

        seed()

        self.assertEqual(Post.all_objects.count(), len(Post.Type) * len(Post.Status))

    def test_poem_body_keeps_line_breaks_and_spacing(self) -> None:
        seed()

        poem = Post.objects.filter(type=Post.Type.POEM).first()
        assert poem is not None
        self.assertIn("\n    ", poem.body)


@override_settings(DEBUG=False)
class DevelopmentCommandGuardTests(TestCase):
    def test_seed_refuses_to_run_without_debug(self) -> None:
        with self.assertRaisesMessage(CommandError, "DEBUG=true"):
            seed()

        self.assertFalse(Post.all_objects.exists())
