from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserEditSerializer


class UserProfile(viewsets.ModelViewSet):
    queryset = User.objects.all()
    search_fields = ["first_name"]
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserEditSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    http_method_names = ["get", "patch"]

    def get_object(self):
        pk = self.kwargs.get("pk")
        if pk == "current":
            return self.request.user
        return super().get_object()
