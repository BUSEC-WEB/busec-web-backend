from rest_framework import serializers  # pyright: ignore[reportMissingTypeStubs]


class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    done = serializers.BooleanField(required=False)
