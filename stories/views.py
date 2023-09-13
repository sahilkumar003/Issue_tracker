from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Story
from .serializers import StorySerializer


class StoryViewSet(ModelViewSet):
    queryset = Story.objects.filter(is_deleted=False)
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project_id"]
    pagination_class = LimitOffsetPagination
    http_method_names = ["get", "post", "patch", "delete"]

    def perform_destroy(self, instance):
        instance.soft_delete()
