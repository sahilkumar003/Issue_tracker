from rest_framework.test import APITestCase

from projects.models import Member, Project
from users.models import User


class ProjectModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sahil@gmail.com",
            password="Password@123",
            first_name="Sahil",
            last_name="Kumar",
            dob="2001-08-07",
            id="1",
        )

    def test_create_project(self):
        project = Project.objects.create(
            title="Project 1",
            description="This is a test project",
            owner=self.user,
        )
        self.assertEqual(project.title, "Project 1")
        self.assertEqual(project.description, "This is a test project")
        self.assertEqual(project.owner, self.user)
        self.assertFalse(project.is_deleted)

    def test_project_str_representation(self):
        project = Project.objects.create(
            title="Project 2",
            description="Another test project",
            owner=self.user,
        )
        expected_str = "Project 2"
        self.assertEqual(str(project), expected_str)


class MemberModelTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="sahil@gmail.com",
            password="Password@123",
            first_name="Sahil",
            last_name="Kumar",
            dob="2001-08-07",
            id="1",
        )
        self.user2 = User.objects.create_user(
            email="aman@gmail.com",
            password="Password@123",
            first_name="Aman",
            last_name="Sharma",
            dob="2004-03-05",
            id="1",
        )
        self.project = Project.objects.create(
            title="Project 1",
            description="This is a test project",
            owner=self.user1,
        )

    def test_create_member(self):
        member = Member.objects.create(user=self.user2, project=self.project)
        self.assertEqual(member.user, self.user2)
        self.assertEqual(member.project, self.project)
        self.assertEqual(member.role, 2)

    def test_member_str_representation(self):
        member = Member.objects.create(user=self.user2, project=self.project)
        expected_str = f"{self.user2.first_name} {self.user2.last_name} - {self.project.title}"
        self.assertEqual(str(member), expected_str)
