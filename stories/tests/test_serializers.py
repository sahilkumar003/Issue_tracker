from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from issue_tracker.settings import EMAIL_HOST_USER
from projects.models import Project
from stories.models import Story
from stories.serializers import StorySerializer
from users.models import User


class StorySerializerTest(TestCase):
    def setUp(self):
        self.project_owner = User.objects.create_user(
            email="owner@gmail.com",
            password="Password@123",
        )
        self.assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.project_owner,
        )

    def test_create_story_with_valid_data(self):
        data = {
            "title": "New Story",
            "description": "This is a new story",
            "assignee": self.assignee.id,
            "estimate": 3,
            "project": self.project.id,
            "status": 1,
            "is_scheduled": 2,
        }
        serializer = StorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        story = serializer.save()

        self.assertEqual(story.title, data["title"])
        self.assertEqual(story.description, data["description"])
        self.assertEqual(story.assignee, self.assignee)
        self.assertEqual(story.estimate, data["estimate"])
        self.assertEqual(story.project, self.project)
        self.assertEqual(story.status, data["status"])
        self.assertEqual(story.is_scheduled, data["is_scheduled"])

    def test_create_story_with_invalid_data(self):
        data = {
            "title": "",
            "description": "This is a new story",
            "assignee": self.assignee.id,
            "estimate": 3,
            "project": self.project.id,
            "status": 1,
            "is_scheduled": 2,
        }
        serializer = StorySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_story_with_assignee_email_notification(self):
        data = {
            "title": "New Story",
            "description": "This is a new story",
            "assignee": self.assignee.id,
            "estimate": 3,
            "project": self.project.id,
            "status": 1,
            "is_scheduled": 2,
        }
        with patch("stories.serializers.send_mail") as mock_send_mail:
            serializer = StorySerializer(data=data)
            self.assertTrue(serializer.is_valid())
            story = serializer.save()

            mock_send_mail.assert_called_once_with(
                "You have been assigned a story",
                f"You have been assigned with the story '{story.title}' in project '{story.project.title}'.",
                EMAIL_HOST_USER,
                [self.assignee.email],
            )

    def test_update_story_with_valid_data(self):
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=self.assignee,
            estimate=5,
            project=self.project,
            status=1,
            is_scheduled=2,
        )

        updated_data = {
            "title": "Updated Story",
            "description": "This is an updated story",
            "assignee": self.assignee.id,
            "estimate": 8,
            "project": self.project.id,
            "status": 2,
            "is_scheduled": 1,
        }

        serializer = StorySerializer(instance=story, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_story = serializer.save()

        self.assertEqual(updated_story.title, updated_data["title"])
        self.assertEqual(updated_story.description, updated_data["description"])
        self.assertEqual(updated_story.assignee, self.assignee)
        self.assertEqual(updated_story.estimate, updated_data["estimate"])
        self.assertEqual(updated_story.project, self.project)
        self.assertEqual(updated_story.status, updated_data["status"])
        self.assertEqual(updated_story.is_scheduled, updated_data["is_scheduled"])

    def test_update_delivered_story(self):
        story = Story.objects.create(
            title="Delivered Story",
            description="This is a delivered story",
            assignee=self.assignee,
            estimate=5,
            project=self.project,
            status=4,
            is_scheduled=2,
        )

        updated_data = {
            "title": "Updated Story",
            "description": "This is an updated story",
            "assignee": self.assignee.id,
            "estimate": 8,
            "project": self.project.id,
            "status": 3,
            "is_scheduled": 2,
        }

        serializer = StorySerializer(instance=story, data=updated_data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertTrue("Delivered stories cannot be updated." in str(context.exception))

    def test_update_started_story_to_unscheduled(self):
        story = Story.objects.create(
            title="Started Story",
            description="This is a started story",
            assignee=self.assignee,
            estimate=5,
            project=self.project,
            status=2,
            is_scheduled=1,
        )

        updated_data = {
            "is_scheduled": 2,
        }

        serializer = StorySerializer(instance=story, data=updated_data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertTrue("Started/Finished stories cannot be unscheduled." in str(context.exception))

    def test_update_finished_story_to_unscheduled(self):
        story = Story.objects.create(
            title="Started Story",
            description="This is a started story",
            assignee=self.assignee,
            estimate=5,
            project=self.project,
            status=3,
            is_scheduled=1,
        )

        updated_data = {
            "is_scheduled": 2,
        }

        serializer = StorySerializer(instance=story, data=updated_data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertTrue("Started/Finished stories cannot be unscheduled." in str(context.exception))

    def test_update_finished_story_with_changed_assignee(self):
        story = Story.objects.create(
            title="Finished Story",
            description="This is a finished story",
            assignee=self.assignee,
            estimate=5,
            project=self.project,
            status=3,
            is_scheduled=1,
        )

        new_assignee = User.objects.create_user(
            email="new_assignee@gmail.com",
            password="Password@123",
        )

        updated_data = {
            "assignee": new_assignee.id,
        }

        serializer = StorySerializer(instance=story, data=updated_data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertTrue(
            "Assignee cannot be changed for stories with status finished or Delivered." in str(context.exception)
        )

    def test_change_assignee_delivered_story(self):
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=self.assignee,
            estimate=5,
            project=self.project,
            status=4,
            is_scheduled=1,
        )

        new_assignee = User.objects.create_user(
            email="new_assignee@gmail.com",
            password="Password@123",
        )

        updated_data = {
            "assignee": new_assignee.id,
        }

        serializer = StorySerializer(instance=story, data=updated_data, partial=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertTrue(
            "Assignee cannot be changed for stories with status finished or Delivered." in str(context.exception)
        )
