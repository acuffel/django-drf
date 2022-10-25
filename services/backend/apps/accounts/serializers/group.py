from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = [
            "url",
            "name",
            "permissions",
            "user_set",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "accounts_api:groups-detail",
                "lookup_field": "pk",
            },
            "permissions": {
                "view_name": "accounts_api:permissions-detail",
                "lookup_field": "pk",
            },
            "user_set": {
                "view_name": "accounts_api:users-detail",
                "lookup_field": "pk",
            },
        }
