from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from projects.models import Member, Project
from users.models import User


class ProjectViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sahil@gmail.com",
            password="Password@123",
            first_name="Sahil",
            last_name="Kumar",
            dob="2001-08-07",
            id="1",
        )

    def set_authenticated_header(self, email, password):
        self.client.login(email=email, password=password)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_project(self):
        data = {
            "title": "Test Project",
            "description": "This is a test project",
            "members": [self.user.id],
        }
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.post(reverse("projects-list"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 1)

    def test_create_project_with_invalid_data(self):
        data = {
            "title": "",
            "description": "This is a test project",
            "members": [self.user.id],
        }
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.post(reverse("projects-list"), data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_project(self):
        other_user = User.objects.create_user(
            email="other@gmail.com",
            password="Other@123",
            first_name="Other",
            last_name="User",
            dob="2000-01-01",
            id="2",
        )
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        data = {
            "description": "Updated project description",
            "updatedMembers": [other_user.id],
        }

        Member.objects.create(user=self.user, project=project)
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.put(
            reverse("projects-detail", kwargs={"pk": project.pk}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        updated_project = Project.objects.get(id=project.id)
        updated_member_ids = updated_project.members.values_list("id", flat=True)
        self.assertEqual(list(updated_member_ids), [other_user.id])
        self.assertNotEqual(list(updated_member_ids), [self.user.id])

    def test_update_project_with_invalid_permissions(self):
        other_user = User.objects.create_user(
            email="other@gmail.com",
            password="Other@123",
            first_name="Other",
            last_name="User",
            dob="2000-01-01",
            id="2",
        )
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=other_user,
        )
        data = {
            "title": "Updated Project Title",
            "description": "Updated project description",
            "members": [self.user.id],
        }
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.put(
            reverse("projects-detail", kwargs={"pk": project.pk}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_list_owned_projects(self):
        Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=self.user,
        )
        other_user = User.objects.create_user(
            email="other@gmail.com",
            password="Other@123",
            first_name="Other",
            last_name="User",
            dob="2000-01-01",
            id="2",
        )
        Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=other_user,
        )
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.get(reverse("projects-list"), {"filter_param": "owned"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_member_projects(self):
        other_user = User.objects.create_user(
            email="other@example.com",
            password="Other@123",
            first_name="Other",
            last_name="User",
            dob="2000-01-01",
            id="2",
        )
        project = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=other_user,
        )
        Member.objects.create(user=self.user, project=project)
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.get(reverse("projects-list"), {"filter_param": "member"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_all_projects(self):
        Project.objects.create(
            title="Test Project 1",
            description="This is a test project 1",
            owner=self.user,
        )
        other_user = User.objects.create_user(
            email="other@example.com",
            password="Other@123",
            first_name="Other",
            last_name="User",
            dob="2000-01-01",
            id="2",
        )
        project2 = Project.objects.create(
            title="Test Project",
            description="This is a test project",
            owner=other_user,
        )
        Member.objects.create(user=self.user, project=project2)
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.get(reverse("projects-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
