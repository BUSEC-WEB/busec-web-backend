from django.db import models

from shared.models import TimeStampedModel
from shared.storage import StorageAlias

# PRD requirements for this slice:
# - Issue: title, cover, issue date, short description, PDF file (§5.3)
# - Archive listing of past issues; PDF download fallback (§5.3)


class MagazineIssue(TimeStampedModel):
    title = models.CharField(max_length=255)
    cover = models.FileField(
        upload_to="magazine/covers/", storage=StorageAlias("cover_images")
    )
    issue_date = models.DateField()
    description = models.TextField(blank=True)
    pdf = models.FileField(
        upload_to="magazine/pdfs/", storage=StorageAlias("magazine_pdfs")
    )

    class Meta(TimeStampedModel.Meta):
        ordering = ("-issue_date",)

    def __str__(self) -> str:
        return self.title
