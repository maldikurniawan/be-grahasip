from cms_app.models import MasterFile
from django.http import JsonResponse, HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.db.models import Q
import json
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from cms_app.serializers import MasterfileSerializer
from cms_app.models import MasterFile
from cms_app.paginations import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from backend_gsip.permissions import PermissionMixin


class MasterfileListAPI(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = MasterFile.objects.all()
    serializer_class = MasterfileSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = "__all__"

    def get_queryset(self):
        self.permission_check("cms_app.view_masterfile")
        queryset = self.queryset
        return queryset

    def create(self, request, *args, **kwargs):
        self.permission_check("cms_app.add_masterfile")
        request_data = self.request.POST.copy()
        if "file" not in request.FILES:
            return Response(
                {"file": "File is Required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validasi tipe file yang diunggah
        allowed_types = [
            "jpeg",
            "png",
            "webp",
            "jpg",
            "JPEG",
            "PNG",
            "WEBP",
            "JPG",
            "pdf",
            "PDF",
            "doc",
            "docx",
            "DOC",
            "DOCX",
        ]
        allowed_types_str = ", ".join(allowed_types)
        max_size = 5 * 1024 * 1024  # 5 MB dalam bytes
        uploaded_file = request.FILES["file"]

        # Create File
        ext = uploaded_file.name.split(".")[-1].lower()
        if ext not in allowed_types:
            return Response(
                {
                    "File ": f"Tipe file {ext} tidak diizinkan. yang di izinkan hanya {allowed_types_str}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if uploaded_file.size > max_size:
            return Response(
                {"File ": "Ukuran file terlalu besar. Maksimal 5 MB."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request_data["size"] = uploaded_file.size
        request_data["type"] = ext
        request_data["file"] = self.request.FILES["file"]

        request_data["created_by"] = self.request.user.pk
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "MasterFile Created",
            "data": serializer.data,
        }
        return Response(response)


class MasterfileAPIView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = MasterFile.objects.all()
    serializer_class = MasterfileSerializer
    pagination_class = CustomPagination
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        self.permission_check("cms_app.change_masterfile")
        instance = self.get_object()
        request_data = self.request.POST.copy()
        if "file" in request.FILES:
            # Validasi tipe file yang diunggah
            allowed_types = [
                "jpeg",
                "png",
                "webp",
                "jpg",
                "JPEG",
                "PNG",
                "WEBP",
                "JPG",
                "pdf",
                "PDF",
                "doc",
                "docx",
                "DOC",
                "DOCX",
            ]
            allowed_types_str = ", ".join(allowed_types)
            max_size = 5 * 1024 * 1024  # 5 MB dalam bytes
            uploaded_file = request.FILES["file"]

            # Create File
            ext = uploaded_file.name.split(".")[-1].lower()
            if ext not in allowed_types:
                return Response(
                    {
                        "File ": f"Tipe file {ext} tidak diizinkan. yang di izinkan hanya {allowed_types_str}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if uploaded_file.size > max_size:
                return Response(
                    {"File ": "Ukuran file terlalu besar. Maksimal 5 MB."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request_data["size"] = uploaded_file.size
            request_data["type"] = ext
            request_data["file"] = self.request.FILES["file"]

        request_data["updated_by"] = self.request.user.pk
        serializer = self.get_serializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "MasterFile Updated",
            "data": serializer.data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        self.permission_check("cms_app.delete_masterfile")
        try:
            instance = self.get_object()
            instance.delete()
            response = {
                "status": status.HTTP_200_OK,
                "message": "MasterFile Deleted",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
