from django.urls import URLPattern, URLResolver
from rest_framework.routers import SimpleRouter

app_name = "committee"

router = SimpleRouter()

urlpatterns: list[URLResolver | URLPattern] = [*router.urls]
