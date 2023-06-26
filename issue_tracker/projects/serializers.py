from rest_framework import serializers
from .models import Project, Member
from users.serializers import UserSerializer
from users.models import User


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ["id", "user", "project", "role"]


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), default=serializers.CurrentUserDefault()
    )
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "owner",
            "members",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        owner_id = self.context["request"].user.id
        validated_data["owner_id"] = owner_id
        return super().create(validated_data)
