from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Staff account. Readers don't sign in, so every user is staff (PRD §3)."""

    class Role(models.TextChoices):
        JOURNALIST = "journalist"
        EXECUTIVE = "executive"
        SITE_ADMIN = "site_admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.JOURNALIST)
