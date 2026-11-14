from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from shared.views import HealthView

API_V1_SLICES = ("accounts", "content", "magazine", "committee", "newsletter")

api_v1: list[URLResolver | URLPattern] = [
    path(f"{slice_name}/", include(f"features.{slice_name}.urls"))
    for slice_name in API_V1_SLICES
]

urlpatterns: list[URLResolver | URLPattern] = [
    path("admin/", admin.site.urls),
    # System health and documentation web addresses never change their version numbers, ensuring monitoring tools and help links never break during updates
    path("api/health/", HealthView.as_view(), name="health"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/", include(api_v1)),
]
