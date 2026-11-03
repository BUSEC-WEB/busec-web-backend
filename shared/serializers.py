from rest_framework import serializers


class HealthChecksSerializer(serializers.Serializer):
    database = serializers.CharField(help_text='"ok" or "error"')


class HealthSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["ok", "error"])
    checks = HealthChecksSerializer()
