from rest_framework import viewsets

from assemblies.models import Assession
from assemblies.serializers import AssessionSerializer

class AssessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assession.objects.all()
    serializer_class = AssessionSerializer
