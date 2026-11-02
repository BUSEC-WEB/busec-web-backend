from django.db import DatabaseError, connection
from django.http import HttpRequest, JsonResponse


def _check_database() -> str:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return "ok"
    except DatabaseError:
        return "error"


def health(request: HttpRequest) -> JsonResponse:
    """For uptime monitoring (PRD §6). Returns 503 if any integration is down."""
    checks = {"database": _check_database()}
    healthy = all(result == "ok" for result in checks.values())
    return JsonResponse(
        {"status": "ok" if healthy else "error", "checks": checks},
        status=200 if healthy else 503,
    )
