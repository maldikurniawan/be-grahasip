# serializers.py
from rest_framework import serializers
from cms_app.models import Article
from django.contrib.auth.models import User


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "image",
            "content",
            "slug",
            "author",
            "status",
            "created_at",
            "updated_at",
        ]
