from django.db import DatabaseError, connection
from django.http import HttpRequest, JsonResponse
from django.core.cache import cache


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


def health(request: HttpRequest) -> JsonResponse:
    """For uptime monitoring (PRD §6). Returns 503 if any integration is down."""
    checks = {"database": _check_database()}
    healthy = all(result == "ok" for result in checks.values())

    return JsonResponse(
        {"status": "ok" if healthy else "error", "checks": checks},
        status=200 if healthy else 503,
    )
