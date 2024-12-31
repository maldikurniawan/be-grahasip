from django.urls import path
from cms_app.views import *

urlpatterns = [
    path("dashboard/", DashboardViewApi.as_view()),
    path("article/", ArticleListApi.as_view()),
    path("article/<int:pk>/", ArticleAPIView.as_view()),
    path("article/posts/<slug:slug>/", SlugArticleApiView.as_view()),
    path("team/", TeamListApi.as_view()),
    path("team/<int:pk>/", TeamAPIView.as_view()),
    path("visitor/", VisitorListAPI.as_view()),
    path("visitor/<int:pk>/", VisitorAPIView.as_view()),
    path("masterfile/", MasterfileListAPI.as_view()),
    path("masterfile/<int:pk>/", MasterfileAPIView.as_view()),
]
