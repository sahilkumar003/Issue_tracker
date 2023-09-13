from django.test import TestCase

from projects.models import Project
from stories.models import Story
from users.models import User


class StoryModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sahil@gmail.com",
            password="Password@123",
            first_name="Sahil",
            last_name="Kumar",
            dob="2001-08-07",
            id=1,
        )

        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
            id=1,
        )

        self.story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=self.user,
            estimate=5,
            project=self.project,
            status=2,
            is_scheduled=1,
            id=1,
        )

    def test_story_creation(self):
        story = Story.objects.get(id=1)
        self.assertEqual(story.title, "Test Story")
        self.assertEqual(story.description, "This is a test story")
        self.assertEqual(story.assignee, self.user)
        self.assertEqual(story.estimate, 5)
        self.assertEqual(story.project, self.project)
        self.assertEqual(story.status, 2)
        self.assertEqual(story.is_scheduled, 1)
        self.assertFalse(story.is_deleted)

    def test_story_soft_delete(self):
        story = Story.objects.get(id=1)
        story.soft_delete()

        deleted_story = Story.objects.get(id=1)
        self.assertTrue(deleted_story.is_deleted)

    def test_story_string_representation(self):
        self.assertEqual(str(self.story), "Test Story")
