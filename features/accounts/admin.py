from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from features.accounts.models import User


@admin.register(User)
class StaffUserAdmin(UserAdmin):  # pyright: ignore[reportMissingTypeArgument]
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    fieldsets = (*(UserAdmin.fieldsets or ()), ("Role", {"fields": ("role",)}))
