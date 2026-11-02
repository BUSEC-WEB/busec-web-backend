from django.contrib import admin
from django.http import JsonResponse
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health(request):
    """For uptime monitoring (PRD §6)."""
    return JsonResponse({"status": "ok"})


urlpatterns: list[URLResolver | URLPattern] = [
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Each feature slice registers its own routes here.
    path("api/todos/", include("features.todos.urls")),
]
