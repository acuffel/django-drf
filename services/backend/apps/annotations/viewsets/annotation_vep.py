from rest_framework import viewsets

from annotations.models import AnnotationVEP
from annotations.serializers import AnnotationVEPSerializer


class AnnotationVEPViewSet(viewsets.ModelViewSet):

    serializer_class = AnnotationVEPSerializer
    queryset = AnnotationVEP.objects.all()
