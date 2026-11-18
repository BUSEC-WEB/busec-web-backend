from rest_framework.serializers import ModelSerializer

from features.accounts.models import User


class MeSerializer(ModelSerializer[User]):
    """The signed-in staff member, so the client tailors the UI to their role."""

    class Meta:  # type: ignore
        model = User  # pyright: ignore[reportAssignmentType]
        fields = ("id", "username", "email", "first_name", "last_name", "role")
        read_only_fields = fields
