from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import InMemoryStorage, Storage
from django.test import SimpleTestCase, override_settings

from features.content.models import Post
from features.magazine.models import MagazineIssue
from shared.env import settings as env
from shared.storage import StorageAlias

IN_MEMORY = {"BACKEND": "django.core.files.storage.InMemoryStorage"}


class StorageAliasTests(SimpleTestCase):
    @override_settings(STORAGES={**settings.STORAGES, "test_bucket": IN_MEMORY})
    def test_resolves_the_configured_storage(self) -> None:
        storage = StorageAlias("test_bucket")()

        self.assertIsInstance(storage, InMemoryStorage)

    @override_settings(STORAGES={**settings.STORAGES, "test_bucket": IN_MEMORY})
    def test_resolved_storage_saves_and_reads_files(self) -> None:
        storage: Storage = StorageAlias("test_bucket")()

        name = storage.save("issue.pdf", ContentFile(b"%PDF-1.7"))

        with storage.open(name) as stored:
            self.assertEqual(stored.read(), b"%PDF-1.7")

    def test_deconstructs_to_the_alias_only(self) -> None:
        path, args, kwargs = StorageAlias("magazine_pdfs").deconstruct()

        self.assertEqual(path, "shared.storage.StorageAlias")
        self.assertEqual(args, ("magazine_pdfs",))
        self.assertEqual(kwargs, {})

    def test_equal_when_the_alias_matches(self) -> None:
        self.assertEqual(StorageAlias("a"), StorageAlias("a"))
        self.assertNotEqual(StorageAlias("a"), StorageAlias("b"))


class S3SettingsTests(SimpleTestCase):
    def test_magazine_files_use_their_own_buckets(self) -> None:
        pdf = MagazineIssue._meta.get_field("pdf")
        cover = MagazineIssue._meta.get_field("cover")

        self.assertEqual(pdf.deconstruct()[3]["storage"], StorageAlias("magazine_pdfs"))
        self.assertEqual(
            cover.deconstruct()[3]["storage"], StorageAlias("cover_images")
        )

    def test_post_cover_images_share_the_cover_bucket(self) -> None:
        cover = Post._meta.get_field("cover_image")

        self.assertEqual(
            cover.deconstruct()[3]["storage"], StorageAlias("cover_images")
        )

    def test_buckets_point_at_the_configured_names(self) -> None:
        self.assertEqual(
            settings.STORAGES["magazine_pdfs"]["OPTIONS"]["bucket_name"],
            env.S3_MAGAZINE_BUCKET,
        )
        self.assertEqual(
            settings.STORAGES["cover_images"]["OPTIONS"]["bucket_name"],
            env.S3_COVER_IMAGE_BUCKET,
        )

    def test_file_urls_are_signed_and_expire(self) -> None:
        self.assertTrue(settings.AWS_QUERYSTRING_AUTH)
        self.assertEqual(settings.AWS_QUERYSTRING_EXPIRE, 3600)

    def test_uploads_never_replace_existing_files(self) -> None:
        self.assertFalse(settings.AWS_S3_FILE_OVERWRITE)
