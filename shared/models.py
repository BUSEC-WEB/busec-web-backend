from collections.abc import Iterable
from datetime import datetime
from typing import Any, Self, TypeVar

from django.db.models import Model, DateTimeField, QuerySet, Manager
from django.utils import timezone

_M = TypeVar("_M", bound=Model)


class TimeStampedModel(Model):
    """Adds `created_at` and `updated_at`, maintained automatically."""

    created_at: DateTimeField[datetime] = DateTimeField(
        auto_now_add=True, editable=False
    )
    updated_at: DateTimeField[datetime] = DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    def save(
        self,
        *args: Any,
        update_fields: Iterable[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """`auto_now` only fires for fields being written, so a partial save
        would otherwise leave `updated_at` stale."""
        if update_fields is not None:
            update_fields = {*update_fields, "updated_at"}
        super().save(*args, update_fields=update_fields, **kwargs)


class SoftDeleteQuerySet(QuerySet[_M]):
    def alive(self) -> Self:
        return self.filter(deleted_at__isnull=True)

    def deleted(self) -> Self:
        return self.filter(deleted_at__isnull=False)


class SoftDeleteManager(Manager[_M]):
    """Default manager: soft-deleted rows are invisible unless asked for."""

    def get_queryset(self) -> SoftDeleteQuerySet[_M]:
        return SoftDeleteQuerySet(
            self.model, using=self._db
        ).alive()  # pyright: ignore[reportUnknownVariableType]


class SoftDeleteModel(Model):
    """Rows are hidden instead of removed, so they can be restored (PRD §5.2).

    `objects` excludes soft-deleted rows; `all_objects` sees everything.
    """

    deleted_at: DateTimeField[datetime | None] = DateTimeField(
        null=True, blank=True, editable=False, db_index=True
    )

    objects = SoftDeleteManager()  # pyright: ignore[reportUnknownVariableType]
    all_objects = SoftDeleteQuerySet.as_manager()  # type: ignore

    class Meta:
        abstract = True

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        if self.is_deleted:
            return
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self) -> None:
        if not self.is_deleted:
            return
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])
