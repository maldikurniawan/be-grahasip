# serializers.py
from rest_framework import serializers
from cms_app.models import Article
from django.contrib.auth.models import User


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False},
        }
