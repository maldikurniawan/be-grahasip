# views.py
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from cms_app.models import Article
from cms_app.paginations import CustomPagination
from cms_app.serializers import ArticleSerializer
from backend_gsip.permissions import PermissionMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ArticleListApi(PermissionMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = "__all__"
    ordering_fields = "__all__"

    def post(self, request, *args, **kwargs):
        # Ensure the request data is valid
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Automatically assign the logged-in user as the author
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Retrieve the list of articles
        articles = Article.objects.all()
        serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data)


class ArticleAPIView(PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        """Retrieve the article object by its primary key (id)."""
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        # Retrieve a single article by ID
        article = self.get_object(pk)
        if article is not None:
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        # Update an existing article by ID
        article = self.get_object(pk)
        if article is not None:
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid():
                # Ensure the author is not updated and is kept as the current user
                serializer.save(author=article.author)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        # Delete an article by ID
        article = self.get_object(pk)
        if article is not None:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
