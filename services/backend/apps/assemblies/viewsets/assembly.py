from rest_framework import viewsets

from assemblies.models import Assembly
from assemblies.serializers import AssemblySerializer

class AssemblyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
