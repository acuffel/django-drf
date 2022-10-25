from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "accounts_api:users-detail",
                "lookup_field": "pk",
            },
            "groups": {
                "view_name": "accounts_api:groups-detail",
                "lookup_field": "pk",
            },
            "user_permissions": {
                "view_name": "accounts_api:permissions-detail",
                "lookup_field": "pk",
            },
        }
