from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    content_type_model = serializers.ReadOnlyField(source="content_type.model")
    content_type_app_label = serializers.ReadOnlyField(source="content_type.app_label")

    class Meta:
        model = Permission
        fields = "__all__"
