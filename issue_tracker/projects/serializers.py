from rest_framework import serializers
from .models import Project, Member
from users.models import User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["user", "project", "role"]


class ProjectSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["title", "description", "owner", "members"]
