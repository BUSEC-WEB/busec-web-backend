from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from shared.views import health

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
    path("api/accounts/", include("features.accounts.urls")),
    path("api/content/", include("features.content.urls")),
    path("api/magazine/", include("features.magazine.urls")),
    path("api/committee/", include("features.committee.urls")),
    path("api/newsletter/", include("features.newsletter.urls")),
]
