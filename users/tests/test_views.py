from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserProfileTestCase(APITestCase):
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

    def test_get_current_user_profile(self):
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.get(reverse("users-detail", kwargs={"pk": "current"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["dob"], self.user.dob)

    def test_get_user_profile(self):
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.get(reverse("users-detail", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["dob"], self.user.dob)

    def test_update_user_profile(self):
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        data = {
            "first_name": "Aman",
            "last_name": "sharma",
            "dob": "2004-03-05",
        }
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.user.id}), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertEqual(response.data["last_name"], data["last_name"])
        self.assertEqual(response.data["dob"], data["dob"])

    def test_update_with_invalid_data(self):
        self.set_authenticated_header(email="test@gmail.com", password="Password123!")
        data = {
            "first_name": "Sumit",
            "last_name": "Tanwar",
            "dob": "2100-01-01",
        }
        response = self.client.patch(
            reverse("users-detail", kwargs={"pk": self.user.pk}),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_unauthenticated(self):
        data = {
            "first_name": "Aman",
            "last_name": "Sharma",
            "dob": "2000-01-01",
        }
        response = self.client.patch(
            reverse("users-detail", kwargs={"pk": self.user.id}),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_get_nonexistent_user_profile(self):
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        response = self.client.get(reverse("users-detail", kwargs={"pk": 901}))
        self.assertEqual(response.status_code, 404)

    def test_get_user_profile_without_authentication(self):
        response = self.client.get(reverse("users-detail", kwargs={"pk": self.user.id}))
        self.assertEqual(response.status_code, 401)

    def test_pagination(self):
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")

        users = []
        for i in range(10):
            user = User.objects.create_user(
                email=f"user{i}@gmail.com",
                password=f"Password@{i}",
                first_name=f"User{i}",
                last_name=f"LastName{i}",
                dob=f"2001-01-{i + 1}",
                id=i + 2,
            )
            users.append(user)

        pagination_limit = 4
        response = self.client.get(reverse("users-list") + f"?limit={pagination_limit}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), pagination_limit)

    def test_search(self):
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")

        response = self.client.get(reverse("users-list"), {"search": "Sahil"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["email"], self.user.email)
        self.assertEqual(response.data[0]["first_name"], self.user.first_name)
