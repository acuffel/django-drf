from rest_framework import serializers

from assemblies.models import Assembly


class AssemblySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assembly
        fields = "__all__"
        extra_kwargs = {
         "url": {
                "view_name": "assemblies_api:assemblies-detail",
                "lookup_field": "pk",
            },
        }
