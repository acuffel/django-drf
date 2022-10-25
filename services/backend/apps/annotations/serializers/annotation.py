from rest_framework import serializers

from annotations.models import Annotation
from assemblies.models import Assembly


class AssemblySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly
        fields = ['pk']


class AnnotationSerializer(serializers.ModelSerializer):

    annotations_vep = serializers.HyperlinkedIdentityField(
        view_name="annotations_api:annotations-detail", lookup_field="pk"
    )

    url = serializers.HyperlinkedIdentityField(
        view_name="annotations_api:annotations-detail", lookup_field="pk"
    )

    assembly = AssemblySerializer(read_only=True)

    class Meta:
        model = Annotation
        fields = [
            "id",
            "url",
            "vcf_file",
            "loading",
            "field_type",
            "annotations_vep",
            "assembly",
        ]
