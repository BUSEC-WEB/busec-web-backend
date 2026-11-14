from drf_spectacular.utils import extend_schema  # type: ignore
from rest_framework.generics import RetrieveAPIView

from features.accounts.models import User
from features.accounts.serializers import MeSerializer


@extend_schema(tags=["accounts"], summary="The signed-in staff member")
class MeView(RetrieveAPIView[User]):
    serializer_class = MeSerializer

    def get_object(self) -> User:
        user = self.request.user
        assert isinstance(user, User)
        return user
