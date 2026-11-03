from django.core.cache import cache
from django.db import DatabaseError, connection
from drf_spectacular.utils import extend_schema
from rest_framework import status as http_status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HealthSerializer


def _check_database() -> str:
    cached_status = cache.get("health_db_status")
    if cached_status:
        return cached_status

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status = "ok"
    except DatabaseError:
        status = "error"

    cache.set("health_db_status", status, timeout=5)
    return status


class HealthView(APIView):
    """For uptime monitoring (PRD §6). Returns 503 if any integration is down."""

    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["health"],
        summary="Service and integration health",
        responses={200: HealthSerializer, 503: HealthSerializer},
    )
    def get(self, request: Request) -> Response:
        checks = {"database": _check_database()}
        healthy = all(result == "ok" for result in checks.values())
        return Response(
            {"status": "ok" if healthy else "error", "checks": checks},
            status=(
                http_status.HTTP_200_OK
                if healthy
                else http_status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )
