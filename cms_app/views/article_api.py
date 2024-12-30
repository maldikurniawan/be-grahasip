from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from cms_app.models import Article
from cms_app.paginations import CustomPagination
from cms_app.serializers import ArticleSerializer
# from backend_gsip.permissions import PermissionMixin


class ArticleListApi(generics.ListCreateAPIView):
    """
    Handles listing and creation of articles.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "title",
    ]
    ordering_fields = "__all__"

    def get_queryset(self):
        """
        Optionally filters the queryset based on request parameters.
        """
        queryset = self.queryset
        return queryset

    def create(self, request, *args, **kwargs):
        # Convert request.data to mutable to avoid QueryDict immutability error
        data = request.data.copy()

        # Add the current user as the author
        data["author"] = request.user.id

        # Check if the image is null or empty and handle accordingly
        if not data.get("image"):
            data.pop("image", None)  # Remove the image field if it's not provided

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "status": status.HTTP_201_CREATED,
            "message": "Article Created Successfully",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_201_CREATED)


class ArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieval, update, and deletion of an article.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        """
        Updates an existing article, ensuring the author remains the same.
        """
        instance = self.get_object()
        # Ensure the author does not change
        if "author" in request.data:
            request.data.pop("author")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Updated Successfully",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Deletes an article.
        """
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Deleted Successfully",
        }
        return Response(response, status=status.HTTP_200_OK)
