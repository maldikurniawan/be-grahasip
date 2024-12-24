from rest_framework import serializers
from cms_app.models import Visitor, IPAddressDetail


class IPAddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPAddressDetail
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    ipaddressdetail = IPAddressDetailSerializer()

    class Meta:
        model = Visitor
        fields = ["id", "ip_address", "ipaddressdetail", "agent", "created_at"]
