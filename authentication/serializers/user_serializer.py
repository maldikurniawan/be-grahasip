from rest_framework import serializers
import hashlib
from django.utils.http import urlencode
from authentication.models import User
import json


class ViewUserSerializer(serializers.ModelSerializer):
    gravatar_url = serializers.SerializerMethodField()
    groups_permissions = serializers.SerializerMethodField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        group_names = [group.name for group in instance.groups.all()]
        representation["groups_name"] = group_names
        representation.pop("password", None)
        return representation

    def get_gravatar_url(self, obj):
        email = obj.email.strip().lower().encode("utf-8")
        email_hash = hashlib.md5(email).hexdigest()
        query_params = urlencode({"s": "200", "d": "identicon"})
        return f"https://www.gravatar.com/avatar/{email_hash}?{query_params}"

    def get_groups_permissions(self, obj):
        unique_permissions = set()
        for group in obj.groups.all():
            for perm in group.permissions.all():
                unique_permissions.add(perm.codename)
        return list(unique_permissions)

    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    gravatar_url = serializers.SerializerMethodField()

    def get_gravatar_url(self, obj):
        email = obj.email.strip().lower().encode("utf-8")
        email_hash = hashlib.md5(email).hexdigest()
        query_params = urlencode({"s": "200", "d": "identicon"})
        return f"https://www.gravatar.com/avatar/{email_hash}?{query_params}"

    class Meta:
        model = User
        fields = "__all__"


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
