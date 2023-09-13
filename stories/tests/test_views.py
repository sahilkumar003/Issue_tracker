from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from projects.models import Project
from stories.models import Story
from users.models import User


class StoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@gmail.com",
            password="Password@123",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_story(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )

        data = {
            "title": "New Story",
            "description": "This is a new story",
            "assignee": assignee.id,
            "estimate": 3,
            "project": project.id,
            "status": 1,
            "is_scheduled": 2,
        }

        response = self.client.post(
            reverse("stories-list"),
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Story.objects.count(), 1)
        self.assertEqual(Story.objects.get().title, "New Story")

    def test_create_story_with_invalid_data(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        data = {
            "title": "",
            "description": "This is a new story",
            "assignee": assignee.id,
            "estimate": 3,
            "project": project.id,
            "status": 1,
            "is_scheduled": 2,
        }

        response = self.client.post(reverse("stories-list"), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_list_stories(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        Story.objects.create(
            title="Story 1",
            description="This is story 1",
            assignee=assignee,
            estimate=3,
            project=project,
            status=1,
            is_scheduled=2,
        )
        Story.objects.create(
            title="Story 2",
            description="This is story 2",
            assignee=assignee,
            estimate=5,
            project=project,
            status=1,
            is_scheduled=1,
        )

        response = self.client.get(reverse("stories-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Story 1")
        self.assertEqual(response.data[1]["title"], "Story 2")

    def test_get_story(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=assignee,
            estimate=5,
            project=project,
            status=1,
            is_scheduled=2,
        )

        response = self.client.get(reverse("stories-detail", args=[story.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Story")

    def test_get_nonexistent_story(self):
        response = self.client.get(reverse("stories-detail", args=[9]))
        self.assertEqual(response.status_code, 404)

    def test_update_story(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=assignee,
            estimate=5,
            project=project,
            status=1,
            is_scheduled=2,
        )
        updated_data = {
            "title": "Updated Story",
            "description": "This is an updated story",
            "assignee": assignee.id,
            "estimate": 8,
            "project": project.id,
            "status": 2,
            "is_scheduled": 1,
        }

        response = self.client.patch(
            reverse("stories-detail", args=[story.id]),
            updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Story.objects.get().title, "Updated Story")

    def test_update_story_with_invalid_data(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=assignee,
            estimate=5,
            project=project,
            status=1,
            is_scheduled=2,
        )
        updated_data = {
            "title": "",
            "description": "This is an updated story",
            "assignee": assignee.id,
            "estimate": 8,
            "project": project.id,
            "status": 2,
            "is_scheduled": 1,
        }

        response = self.client.patch(
            reverse("stories-detail", args=[story.id]),
            updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_nonexistent_story(self):
        new_data = {
            "title": "Updated Story",
            "description": "This is an updated story",
            "estimate": 8,
        }
        response = self.client.patch(reverse("stories-detail", args=[9]), new_data, format="json")
        self.assertEqual(response.status_code, 404)

    def test_delete_story(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=assignee,
            estimate=5,
            project=project,
            status=1,
            is_scheduled=2,
        )

        response = self.client.delete(reverse("stories-detail", args=[story.id]))
        self.assertEqual(response.status_code, 204)

    def test_soft_delete_story_with_update(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=assignee,
            estimate=5,
            project=project,
            status=1,
            is_scheduled=2,
        )
        story.is_deleted = True
        story.save()
        updated_data = {
            "title": "Updated Story",
            "description": "This is an updated story",
            "assignee": assignee.id,
            "estimate": 8,
            "project": project.id,
            "status": 2,
            "is_scheduled": 1,
        }

        response = self.client.patch(
            reverse("stories-detail", args=[story.id]),
            updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_story(self):
        response = self.client.delete(reverse("stories-detail", args=[9]))
        self.assertEqual(response.status_code, 404)

    def test_soft_deleted_story_not_listed(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        story = Story.objects.create(
            title="Test Story",
            description="This is a test story",
            assignee=assignee,
            estimate=5,
            project=project,
            status=1,
            is_scheduled=2,
            is_deleted=True,
        )
        response = self.client.get(reverse("stories-list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(story.id, [item["id"] for item in response.data])

    def test_filter_stories_by_project(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project1 = Project.objects.create(
            title="Project 1",
            description="This is project 1",
            owner=self.user,
        )
        project2 = Project.objects.create(
            title="Project 2",
            description="This is project 2",
            owner=self.user,
        )
        story1 = Story.objects.create(
            title="Story in Project 1",
            description="This is a story in project 1",
            assignee=assignee,
            estimate=5,
            project=project1,
            status=1,
            is_scheduled=2,
        )
        Story.objects.create(
            title="Story in Project 2",
            description="This is a story in project 2",
            assignee=assignee,
            estimate=3,
            project=project2,
            status=1,
            is_scheduled=2,
        )
        response = self.client.get(reverse("stories-list"), {"project_id": project1.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], story1.id)

    def test_pagination(self):
        assignee = User.objects.create_user(
            email="assignee@gmail.com",
            password="Password@123",
        )

        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        [
            Story.objects.create(
                title=f"Story {i}",
                description=f"This is story {i}",
                assignee=assignee,
                estimate=5,
                project=project,
                status=1,
                is_scheduled=2,
            )
            for i in range(10)
        ]

        response = self.client.get(reverse("stories-list") + "?limit=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
