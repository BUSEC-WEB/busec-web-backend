"""Named file storages for model fields.

Buckets are configured once in `settings.STORAGES` (see config/settings.py). A model
field picks one by alias:

    pdf = models.FileField(upload_to="pdfs/", storage=StorageAlias("magazine_pdfs"))

Migrations record only the alias, never the bucket name or credentials, so the same
migration works against MinIO in dev and any S3 provider in production.
"""

from typing import Any

from django.core.files.storage import Storage, storages


class StorageAlias:
    """A zero-argument callable that resolves a `settings.STORAGES` alias."""

    def __init__(self, alias: str) -> None:
        self.alias = alias

    def __call__(self) -> Storage:
        return storages[self.alias]

    def deconstruct(self) -> tuple[str, tuple[str], dict[str, Any]]:
        """How migrations serialise this: by alias, never by bucket or credentials."""
        return ("shared.storage.StorageAlias", (self.alias,), {})

    def __eq__(self, other: object) -> bool:
        return isinstance(other, StorageAlias) and other.alias == self.alias

    def __hash__(self) -> int:
        return hash(self.alias)
