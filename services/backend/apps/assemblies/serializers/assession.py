from rest_framework import serializers

from assemblies.models import Assession


class AssessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assession
        fields = "__all__"
        extra_kwargs = {
         "url": {
                "view_name": "assemblies_api:assessions-detail",
                "lookup_field": "pk",
            },
        "assembly": {
                "view_name": "assemblies_api:assemblies-detail",
                "lookup_field": "pk",
            },
        }
