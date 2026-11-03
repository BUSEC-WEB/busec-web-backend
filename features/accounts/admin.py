from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from features.accounts.models import User


@admin.register(User)
class StaffUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    # UserAdmin.fieldsets is typed as optional, so unpack it instead of using "+".
    fieldsets = (*(UserAdmin.fieldsets or ()), ("Role", {"fields": ("role",)}))
