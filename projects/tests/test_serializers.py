from unittest.mock import Mock, patch

from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from issue_tracker.settings import EMAIL_HOST_USER
from projects.models import Project
from projects.serializers import ProjectSerializer
from users.models import User


class ProjectSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sahil@gmail.com",
            password="Password@123",
            first_name="Sahil",
            last_name="Kumar",
            dob="2001-08-07",
            id="1",
        )

    def test_create_project_valid(self):
        testUser = User.objects.create_user(
            email="test@gmail.com",
            password="Password@123",
            first_name="Test",
            last_name="User",
            dob="2001-08-07",
            id="2",
        )

        data = {
            "title": "Test Project",
            "description": "This is a test project",
            "members": [testUser.id],
        }

        mock_request = Mock()
        mock_request.user = self.user
        mock_request.data = data
        with patch("projects.serializers.send_mail") as mock_send_mail:
            serializer = ProjectSerializer(data=data, context={"request": mock_request})
            self.assertTrue(serializer.is_valid())
            project = serializer.create(serializer.validated_data)

            mock_send_mail.assert_called_once_with(
                "New Project Created",
                f"You have been added to the project '{project.title}'.",
                EMAIL_HOST_USER,
                [testUser.email],
            )

    def test_create_project_invalid(self):
        data = {
            "title": "",
            "description": "",
            "members": [self.user.id],
        }

        mock_request = Mock()
        mock_request.user = self.user
        mock_request.data = data
        serializer = ProjectSerializer(data=data, context={"request": mock_request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("description", serializer.errors)

    def test_update_project_valid(self):
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        serializer = ProjectSerializer(instance=project)
        data = {
            "description": "This is an updated project description",
        }
        updated_project = serializer.update(project, data)
        self.assertEqual(updated_project.description, data["description"])

    def test_update_project_invalid_title_change(self):
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        serializer = ProjectSerializer(instance=project)
        data = {
            "title": "New Title",
            "description": "This is an updated project description",
        }

        with self.assertRaises(ValidationError) as context:
            serializer.update(project, data)
        self.assertTrue("You cannot change the title of the project." in str(context.exception))
