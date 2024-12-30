from rest_framework import serializers
from cms_app.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False},
        }
