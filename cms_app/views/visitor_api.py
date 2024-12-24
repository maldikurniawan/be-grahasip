from cms_app.models import Visitor
from django.http import JsonResponse, HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.db.models import Q
import json
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from cms_app.serializers import VisitorSerializer
from cms_app.models import Visitor, IPAddressDetail
from cms_app.paginations import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions
from django.utils import timezone
from backend_gsip.permissions import PermissionMixin
import requests


class VisitorListAPI(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["ip_address"]
    ordering_fields = "__all__"

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    def create(self, request, *args, **kwargs):
        request_data = {}
        ip_address = request.data.get("ip_address")
        agent = request.data.get("agent")
        request_data["ip_address"] = ip_address
        request_data["agent"] = agent
        ip_address_detail = None

        # Mendapatkan waktu sekarang dan menghitung batas waktu (midnight) hari ini
        now = timezone.now()
        start_of_day = timezone.make_aware(
            timezone.datetime(now.year, now.month, now.day)
        )
        # Mencari Visitor yang sudah ada hari ini
        existing_visitor = Visitor.objects.filter(
            ip_address=ip_address, created_at__gte=start_of_day
        ).first()
        if existing_visitor:
            # Jika visitor sudah ada di hari ini
            return Response(
                {"message": "Visitor already recorded today."},
                status=status.HTTP_200_OK,
            )

        try:
            response = requests.get(f"https://erpskrip.id/api/checkip/{ip_address}")
            response.raise_for_status()  # Memicu exception untuk status error HTTP
            jsonData = response.json()

            # Memastikan field yang diperlukan ada
            if "ip" in jsonData:  # Sesuaikan field sesuai kebutuhan
                # Insert data ke model IPAddressDetail
                ip_address_detail = IPAddressDetail(
                    ip=jsonData.get("ip"),
                    network=jsonData.get("network"),
                    version=jsonData.get("version"),
                    city=jsonData.get("city"),
                    region=jsonData.get("region"),
                    region_code=jsonData.get("region_code"),
                    country=jsonData.get("country"),
                    country_name=jsonData.get("country_name"),
                    country_code=jsonData.get("country_code"),
                    country_code_iso3=jsonData.get("country_code_iso3"),
                    country_capital=jsonData.get("country_capital"),
                    country_tld=jsonData.get("country_tld"),
                    continent_code=jsonData.get("continent_code"),
                    in_eu=jsonData.get("in_eu"),
                    postal=jsonData.get("postal"),
                    latitude=jsonData.get("latitude"),
                    longitude=jsonData.get("longitude"),
                    timezone=jsonData.get("timezone"),
                    utc_offset=jsonData.get("utc_offset"),
                    country_calling_code=jsonData.get("country_calling_code"),
                    currency=jsonData.get("currency"),
                    currency_name=jsonData.get("currency_name"),
                    languages=jsonData.get("languages"),
                    country_area=jsonData.get("country_area"),
                    country_population=jsonData.get("country_population"),
                    asn=jsonData.get("asn"),
                    org=jsonData.get("org"),
                )
                ip_address_detail.save()  # Menyimpan detail IP Address
        except requests.RequestException as e:
            print(
                "di Visitor ip ->",
                ip_address,
                "errornya ->",
                str(e),
            )

        # Jika pengunjung baru, simpan data visitor
        visitor = Visitor(
            ipaddressdetail=ip_address_detail,
            ip_address=ip_address,
            agent=agent,
        )
        visitor.created_at = now
        visitor.save()

        response = {
            "status": status.HTTP_200_OK,
            "message": "New Visitor has been created record ipaddress",
            "data": ip_address,
        }
        return Response(response, status=status.HTTP_200_OK)


class VisitorAPIView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    pagination_class = CustomPagination
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request_data = self.request.POST.copy()
        serializer = self.get_serializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Visitor Updated",
            "data": serializer.data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            response = {
                "status": status.HTTP_200_OK,
                "message": "Visitor Deleted",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
