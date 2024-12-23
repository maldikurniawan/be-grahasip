from authentication.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/", UserListAPI.as_view()),
    path("getuser/", GetUserDetailAPIView.as_view()),
    path("user/<int:pk>/", UserAPIView.as_view()),
    path("permission/", PermissionListAPIView.as_view()),
    path("permissionlist/", PermissionListAPIViewList.as_view()),
    path("permissionlist/<int:pk>/", PermissionAPIView.as_view()),
    path("contenttype/", ContentTypeListAPIView.as_view()),
    path("contenttype/<int:pk>/", ContentTypeAPIView.as_view()),
    path("group/", GroupListAPI.as_view()),
    path("group/<int:pk>/", GroupAPIView.as_view()),
]
