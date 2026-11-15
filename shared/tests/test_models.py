"""TimeStampedModel and SoftDeleteModel, exercised through Post, which uses both."""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from features.content.models import Post
from shared.tests.factories import make_post, make_user


class TimeStampedModelTests(TestCase):
    def setUp(self) -> None:
        self.post = make_post(make_user("author"))

    def test_sets_both_timestamps_on_create(self) -> None:
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)

    def test_partial_save_still_bumps_updated_at(self) -> None:
        an_hour_ago = timezone.now() - timedelta(hours=1)
        Post.objects.filter(pk=self.post.pk).update(updated_at=an_hour_ago)
        self.post.refresh_from_db()

        self.post.title = "Renamed"
        self.post.save(update_fields=["title"])

        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Renamed")
        self.assertGreater(self.post.updated_at, an_hour_ago)

    def test_created_at_does_not_change_on_save(self) -> None:
        created_at = self.post.created_at
        self.post.title = "Renamed"
        self.post.save()

        self.post.refresh_from_db()
        self.assertEqual(self.post.created_at, created_at)


class SoftDeleteModelTests(TestCase):
    def setUp(self) -> None:
        self.author = make_user("author")
        self.post = make_post(self.author)

    def test_new_rows_are_not_deleted(self) -> None:
        self.assertFalse(self.post.is_deleted)
        self.assertIsNone(self.post.deleted_at)

    def test_soft_delete_hides_row_from_default_manager(self) -> None:
        self.post.soft_delete()

        self.assertTrue(self.post.is_deleted)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        self.assertTrue(Post.all_objects.filter(pk=self.post.pk).exists())

    def test_soft_delete_keeps_the_row_in_the_database(self) -> None:
        self.post.soft_delete()

        stored = Post.all_objects.get(pk=self.post.pk)
        self.assertIsNotNone(stored.deleted_at)

    def test_soft_delete_hides_row_from_related_managers(self) -> None:
        self.post.soft_delete()

        self.assertFalse(self.author.posts.exists())

    def test_soft_delete_bumps_updated_at(self) -> None:
        an_hour_ago = timezone.now() - timedelta(hours=1)
        Post.objects.filter(pk=self.post.pk).update(updated_at=an_hour_ago)
        self.post.refresh_from_db()

        self.post.soft_delete()

        stored = Post.all_objects.get(pk=self.post.pk)  # type: ignore
        self.assertGreater(stored.updated_at, an_hour_ago)  # type: ignore

    def test_soft_delete_twice_keeps_the_original_deletion_time(self) -> None:
        self.post.soft_delete()
        first_deleted_at = self.post.deleted_at  # type: ignore

        self.post.soft_delete()

        self.assertEqual(self.post.deleted_at, first_deleted_at)

    def test_restore_brings_the_row_back(self) -> None:
        self.post.soft_delete()

        self.post.restore()

        self.assertFalse(self.post.is_deleted)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_restore_on_a_live_row_is_a_no_op(self) -> None:
        self.post.restore()

        self.assertFalse(self.post.is_deleted)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_all_objects_can_filter_by_state(self) -> None:
        deleted = make_post(self.author, title="Deleted")
        deleted.soft_delete()

        self.assertQuerySetEqual(Post.all_objects.alive(), [self.post])  # type: ignore
        self.assertQuerySetEqual(Post.all_objects.deleted(), [deleted])  # type: ignore
