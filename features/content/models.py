from django.conf import settings
from django.db import models

from shared.models import SoftDeleteModel, TimeStampedModel
from shared.storage import StorageAlias

# PRD requirements for this slice:
# - Types: article, poem, literature (§5.1), one Post model with a `type` field
# - Fields: title, author byline, category, cover image, image credit, body, status, publish date (§5.1)
# - Poem/literature bodies keep line breaks and spacing exactly (§5.1): stored verbatim in `body`;
#   preserving whitespace is a rendering concern for the frontend.
# - featured flag, set by executives (§5.1)
# - Status flow: draft -> submitted -> published, or sent back (§5.2): sent back = back to draft
# - Only executives publish/delete; delete is a soft delete (§5.2)
# - Open question: can journalists edit others' posts? Default: own drafts only (§3)


class Post(TimeStampedModel, SoftDeleteModel):
    class Type(models.TextChoices):
        ARTICLE = "article"
        POEM = "poem"
        LITERATURE = "literature"

    class Status(models.TextChoices):
        DRAFT = "draft"
        SUBMITTED = "submitted"
        PUBLISHED = "published"

    type = models.CharField(max_length=20, choices=Type.choices)
    title = models.CharField(max_length=255)
    author_byline = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    cover_image = models.FileField(
        upload_to="posts/covers/", blank=True, storage=StorageAlias("cover_images")
    )
    image_credit = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    publish_date = models.DateTimeField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="posts"
    )

    class Meta(TimeStampedModel.Meta, SoftDeleteModel.Meta):
        ordering = ("-publish_date", "-created_at")

    def __str__(self) -> str:
        return self.title
