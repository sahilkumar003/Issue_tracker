from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from users.models import User

from .models import Member, Project
from .serializers import ProjectSerializer


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT":
            project = view.get_object()
            return request.user == project.owner
        return True


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    http_method_names = ["get", "post", "put"]

    def perform_create(self, serializer):
        project = serializer.save()
        members = self.request.data.get("members", [])

        for member_id in members:
            user = User.objects.get(id=member_id)
            Member.objects.create(
                user=user,
                project=project,
                role=self.request.data.get(f"member_role_{member_id}", 2),
            )

    def update(self, request, pk=None, *args, **kwargs):
        kwargs["partial"] = True
        project = self.get_object()

        response = super().update(request, *args, **kwargs)

        updated_members = request.data.get("updatedMembers", [])
        current_members = set(Member.objects.filter(project=project).values_list("user_id", flat=True))
        members_to_add = set(updated_members) - current_members
        members_to_remove = current_members - set(updated_members)

        for member_id in members_to_add:
            user = User.objects.get(id=member_id)
            Member.objects.create(
                user=user,
                project=project,
                role=request.data.get(f"member_role_{member_id}", 2),
            )
        Member.objects.filter(project=project, user_id__in=members_to_remove).delete()

        return response

    def list(self, request):
        filter_param = request.query_params.get("filter_param", None)
        user = request.user

        if filter_param == "owned":
            projects = Project.objects.filter(owner=user, is_deleted=False)
        elif filter_param == "member":
            projects = Project.objects.filter(members=user, is_deleted=False)
        else:
            projects = Project.objects.filter(Q(owner=user) | Q(members=user), is_deleted=False).distinct()

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
