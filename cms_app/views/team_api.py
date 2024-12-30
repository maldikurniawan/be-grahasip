from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from cms_app.models import Team
from cms_app.paginations import CustomPagination
from cms_app.serializers import TeamSerializer
# from backend_gsip.permissions import PermissionMixin


class TeamListApi(generics.ListCreateAPIView):
    """
    Handles listing and creation of Teams.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "name",
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

        # Check if the image is null or empty and handle accordingly
        if not data.get("image"):
            data.pop("image", None)  # Remove the image field if it's not provided

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "status": status.HTTP_201_CREATED,
            "message": "Team Created Successfully",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_201_CREATED)


class TeamAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieval, update, and deletion of an Team.
    """

    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = CustomPagination
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Team Updated Successfully",
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Deletes an Team.
        """
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "Team Deleted Successfully",
        }
        return Response(response, status=status.HTTP_200_OK)
