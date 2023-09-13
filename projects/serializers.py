from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    members = UserSerializer(many=True, read_only=True)

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
        members_data = self.context["request"].data.get("members", [])

        recipient_list = [user.email for user in User.objects.filter(id__in=members_data).exclude(id=owner_id)]

        project = super().create(validated_data)

        subject = "New Project Created"
        message = f"You have been added to the project '{project.title}'."
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        return project

    def update(self, instance, validated_data):
        if "title" in validated_data:
            raise serializers.ValidationError({"title": ["You cannot change the title of the project."]})
        description = validated_data.get("description", instance.description)
        instance.description = description

        instance.save()
        return instance
