from django.urls import URLPattern, URLResolver, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from features.accounts.views import MeView

app_name = "accounts"

router = SimpleRouter()

urlpatterns: list[URLResolver | URLPattern] = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    *router.urls,
]
