from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from accounts.models import User
from accounts.serializers import UserSerializer


class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.public_objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
