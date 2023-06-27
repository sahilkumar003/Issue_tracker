from rest_framework import serializers
from stories.models import Story


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "description",
            "assignee",
            "estimate",
            "project",
            "status",
            "is_scheduled",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        ordering = [
            "-status",
            "created_at",
        ]
