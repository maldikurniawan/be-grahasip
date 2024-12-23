from authentication.models import User
from django.http import JsonResponse, HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.db.models import Q
import os
import random
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from authentication.serializers import *
from authentication.models import User, Group
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from utils.utils import *
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from cms_app.paginations import CustomPagination
from backend_gsip.permissions import PermissionMixin


class UserListAPI(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["first_name", "email", "username"]
    ordering_fields = "__all__"

    def list(self, request, *args, **kwargs):
        self.permission_check("auth.view_user")
        # Menggunakan self.get_queryset() untuk mendapatkan queryset
        queryset = self.get_queryset()
        serializer = ViewUserSerializer(queryset, many=True)

        # Terapkan pagination jika diperlukan
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ViewUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        self.permission_check("auth.add_user")
        request_data = self.request.POST.dict()
        if "password" in request_data:
            hashed_password = make_password(request_data["password"])
            request_data["password"] = hashed_password

        request_data["groups"] = [request_data["groups"]]

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response = {
            "status": status.HTTP_200_OK,
            "message": "User Created",
            "data": serializer.data,
        }
        return Response(response)


class UserAPIView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        self.permission_check("auth.view_user")
        instance = self.get_object()
        serializer = ViewUserSerializer(instance)
        encrypted_data = encrypt(serializer.data)
        return Response(encrypted_data)

    def update(self, request, *args, **kwargs):
        self.permission_check("auth.change_user")
        instance = self.get_object()
        request_data = self.request.POST.dict()

        # edit data user in user account atau admin account
        if "password" in request_data:
            hashed_password = make_password(request_data["password"])
            request_data["password"] = hashed_password
        else:
            request_data["password"] = instance.password

        request_data["groups"] = [request_data["groups"]]

        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response = {
            "status": status.HTTP_200_OK,
            "message": "User Updated",
            "data": serializer.data,
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        self.permission_check("auth.delete_user")
        try:
            instance = self.get_object()
            instance.delete()

            response = {
                "status": status.HTTP_200_OK,
                "message": "User Deleted",
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GetUserDetailAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ViewUserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
