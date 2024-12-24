from rest_framework import serializers
from cms_app.models import MasterFile


class MasterfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterFile
        fields = [
            "id",
            "name",
            "file",
            "type",
            "size",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
