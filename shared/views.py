from django.http import HttpRequest, JsonResponse


def health(request: HttpRequest) -> JsonResponse:
    """For uptime monitoring (PRD §6)."""
    return JsonResponse({"status": "ok"})
