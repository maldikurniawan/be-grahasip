from django.contrib.contenttypes.models import ContentType
from authentication.serializers import ContentTypeSerializer
from rest_framework import generics, permissions, status
from django.db import transaction
from rest_framework.response import Response
from cms_app.paginations import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from backend_gsip.permissions import PermissionMixin


class ContentTypeListAPIView(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["app_label", "model"]
    ordering_fields = "__all__"

    def get_queryset(self):
        self.permission_check("contenttypes.view_contenttype")
        # Mengatur pengurutan berdasarkan kolom 'id'
        queryset = self.queryset
        queryset = queryset.order_by("-id")
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        self.permission_check("contenttypes.add_contenttype")
        request_data = self.request.POST.dict()
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Content Type Created",
            "data": serializer.data,
        }
        return Response(response)


class ContentTypeAPIView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        self.permission_check("contenttypes.change_contenttype")
        instance = self.get_object()
        request_data = self.request.POST.dict()
        serializer = self.get_serializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Content Type Updated",
            "data": serializer.data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        self.permission_check("contenttypes.delete_contenttype")
        try:
            instance = self.get_object()
            instance.delete()
            response = {
                "status": status.HTTP_200_OK,
                "message": "Content Type Deleted",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
