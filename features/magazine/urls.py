from django.urls import URLPattern, URLResolver
from rest_framework.routers import SimpleRouter

app_name = "magazine"

router = SimpleRouter()

urlpatterns: list[URLResolver | URLPattern] = [*router.urls]
