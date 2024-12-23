from django.http import JsonResponse, HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.db.models import Q
import json
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from authentication.serializers import GroupSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions
from utils import *
from cms_app.paginations import CustomPagination
from backend_gsip.permissions import PermissionMixin


class GroupListAPI(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = "__all__"

    def get_queryset(self):
        self.permission_check("auth.view_group")
        queryset = self.queryset
        return queryset

    def create(self, request, *args, **kwargs):
        self.permission_check("auth.add_group")
        request_data = self.request.POST.dict()
        request_data["permissions"] = self.request.POST.getlist("permissions[]")

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "status": status.HTTP_200_OK,
            "message": "Group Created",
            "data": serializer.data,
        }
        return Response(response)


class GroupAPIView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        self.permission_check("auth.change_group")
        instance = self.get_object()
        request_data = {}
        request_data["name"] = self.request.POST.get("name")
        request_data["permissions"] = self.request.POST.getlist("permissions[]")
        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response = {
            "status": status.HTTP_200_OK,
            "message": "Group Updated",
            "data": serializer.data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        self.permission_check("auth.delete_group")
        try:
            instance = self.get_object()
            instance.delete()

            response = {
                "status": status.HTTP_200_OK,
                "message": "Group Deleted",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
