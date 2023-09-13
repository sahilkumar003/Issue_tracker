from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers

from stories.models import Story

STATUS = {
    "Not Started": 1,
    "Started": 2,
    "Finished": 3,
    "Delivered": 4,
}

SCHEDULE = {
    "Scheduled": 1,
    "Not Scheduled": 2,
}


class StorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="assignee.get_full_name", read_only=True)

    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "description",
            "assignee",
            "name",
            "estimate",
            "project",
            "status",
            "is_scheduled",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        instance = self.instance
        status = data.get("status")
        is_scheduled = data.get("is_scheduled")
        assignee = data.get("assignee")

        if (
            instance
            and instance.status in [STATUS["Started"], STATUS["Finished"]]
            and status != STATUS["Not Started"]
            and is_scheduled == SCHEDULE["Not Scheduled"]
        ):
            raise serializers.ValidationError(
                {"update": ["Started/Finished stories cannot be unscheduled."]}
            )

        if (
            instance
            and instance.status in [STATUS["Finished"], STATUS["Delivered"]]
            and assignee
            and assignee != instance.assignee
        ):
            raise serializers.ValidationError(
                {
                    "update": [
                        "Assignee cannot be changed for stories with status finished or Delivered."
                    ]
                }
            )

        if instance and instance.status == STATUS["Delivered"]:
            raise serializers.ValidationError(
                {"update": ["Delivered stories cannot be updated."]}
            )
        return data

    def create(self, validated_data):
        story = Story.objects.create(**validated_data)
        assignee = story.assignee

        subject = "You have been assigned a story"
        message = f"You have been assigned with the story '{story.title}' in project '{story.project.title}'."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [assignee.email]
        send_mail(subject, message, email_from, recipient_list)
        return story
