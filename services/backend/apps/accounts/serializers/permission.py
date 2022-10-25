from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        exclude = [
            "content_type",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "accounts_api:permissions-detail",
                "lookup_field": "pk",
            },
        }
