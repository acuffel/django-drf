from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from accounts.serializers import GroupSerializer


class GroupViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
