from typing import Any

from rest_framework.serializers import Serializer, CharField, ChoiceField


class HealthChecksSerializer(Serializer[dict[str, Any]]):
    database = CharField(help_text='"ok" or "error"')


class HealthSerializer(Serializer[dict[str, Any]]):
    status = ChoiceField(choices=["ok", "error"])
    checks = HealthChecksSerializer()
