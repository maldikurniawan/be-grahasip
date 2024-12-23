from django.contrib.auth.models import Permission
from authentication.serializers import PermissionSerializer
from rest_framework import generics, permissions, status
from django_filters import rest_framework as filters
from django.db import transaction
from rest_framework.response import Response
from cms_app.paginations import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from backend_gsip.permissions import PermissionMixin


class PermissionListAPIViewList(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "codename"]
    ordering_fields = "__all__"

    def get_queryset(self):
        self.permission_check("auth.view_permission")
        content_type_id = self.request.GET.get("content_type")
        if content_type_id:
            queryset = Permission.objects.filter(content_type=content_type_id)
        else:
            queryset = Permission.objects.all()
        # Mengatur pengurutan berdasarkan kolom 'id'
        queryset = queryset.order_by("-id")
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        self.permission_check("auth.add_permission")
        request_data = self.request.POST.dict()
        request_data["name"] = self.request.POST.get("codename")
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Permission Created",
            "data": serializer.data,
        }
        return Response(response)


class PermissionListAPIView(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PermissionSerializer

    def get_queryset(self):
        self.permission_check("auth.view_permission")
        content_type_id = self.request.GET.get("content_type")
        if content_type_id:
            queryset = Permission.objects.filter(content_type=content_type_id)
        else:
            queryset = Permission.objects.all()
        # Mengatur pengurutan berdasarkan kolom 'id'
        queryset = queryset.order_by("id")
        return queryset


class PermissionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        self.permission_check("auth.change_permission")
        instance = self.get_object()
        request_data = self.request.POST.dict()
        request_data["name"] = self.request.POST.get("codename")
        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Permission Updated",
            "data": serializer.data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        self.permission_check("auth.delete_permission")
        try:
            instance = self.get_object()
            instance.delete()
            response = {
                "status": status.HTTP_200_OK,
                "message": "Permission Deleted",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
