import logging
from multiprocessing import context

from pathlib import Path
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from annotations.models import Annotation, AnnotationVEP
from assemblies.models import Assembly
from annotations.serializers import (
    AnnotationSerializer,
    AnnotationVEPSerializer,
)
from core.tasks import load_annotation

logger = logging.getLogger(__name__)


class AnnotationViewSet(viewsets.ModelViewSet):

    serializer_class = AnnotationSerializer
    queryset = Annotation.objects.all()

    def create(self, request):
        vcf_file = request.FILES["vcf_file"]
        assembly_id = request.data.get("assembly")
        field_type = request.data.get("field_type")
        assembly = Assembly.objects.get(pk=assembly_id)
        annotation = Annotation.objects.create(
            assembly=assembly,
            field_type=field_type,
        )
        annotation.vcf_file = vcf_file
        annotation.save()
        
        logger.info(f'Run annotation: {annotation}')

        load_annotation.delay(annotation_pk=annotation.pk)

        serializer_context = {
            "request": request,
        }
        serializer = self.serializer_class(
            data={'annotation': annotation},
            context=serializer_context,
        )
        if serializer.is_valid():
            return Response({'id': annotation.pk}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["get"],
        detail=True,
        url_path="annotations-vep",
        url_name="annotations_vep",
    )
    def annotations_vep(self, request, pk=None):
        annotation = Annotation.objects.get(pk=self.kwargs["pk"])
        queryset = AnnotationVEP.objects.filter(annotation=annotation)
        serializer = AnnotationVEPSerializer(queryset, many=True)
        return Response(serializer.data)
