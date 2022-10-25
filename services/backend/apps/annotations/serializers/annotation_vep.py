from rest_framework import serializers

from annotations.models import AnnotationVEP


class AnnotationVEPSerializer(serializers.ModelSerializer):

    #Add field_type in fields

    class Meta:
        model = AnnotationVEP
        fields = [
            "id",
            "metadata",
            "annotation",
        ]
