from unittest.mock import patch

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from issue_tracker.settings import EMAIL_HOST_USER
from users.models import User


class SignupViewTestCase(APITestCase):
    def test_signup_valid_data(self):
        data = {
            "email": "sahil@gmail.com",
            "password": "Password@123",
            "first_name": "Sahil",
            "last_name": "Kumar",
            "dob": "2001-08-07",
            "confirm_password": "Password@123",
        }

        with patch("authentication.views.send_mail") as mock_send_mail:
            response = self.client.post(reverse("signup"), data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data["message"],
                ["Account has been successfully created."],
            )
            self.assertTrue("access_token" in response.data)
            mock_send_mail.assert_called_once_with(
                "Welcome to the Issue Tracker System",
                "Hi Sahil, thank you for registering in the Issue Tracker System",
                EMAIL_HOST_USER,
                ["sahil@gmail.com"],
            )

    def set_authenticated_header(self, email, password):
        self.user = User.objects.create_user(
            email=email,
            password=password,
        )
        self.client.login(email=email, password=password)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_signup_invalid_data(self):
        data = {
            "email": "invalid_email",
            "password": "password",
            "first_name": "",
            "last_name": "",
            "dob": "2026-05-04",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("email" in response.data)
        self.assertTrue("password" in response.data)
        self.assertTrue("first_name" in response.data)
        self.assertTrue("last_name" in response.data)
        self.assertTrue("dob" in response.data)

    def test_signup_authenticated_user(self):
        self.set_authenticated_header(email="sahil@gmail.com", password="Password@123")
        data = {
            "email": "test@example.com",
            "password": "Password123!",
            "first_name": "Sahil",
            "last_name": "Kumar",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 403)


class SigninViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sahil@gmail.com",
            password="Sahil@123",
        )

    def test_signin_valid_credentials(self):
        data = {
            "email": "sahil@gmail.com",
            "password": "Sahil@123",
        }
        response = self.client.post(reverse("signin"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], ["Logged in successfully."])
        self.assertTrue("access_token" in response.data)

    def test_signin_invalid_credentials(self):
        data = {
            "email": "user@example.com",
            "password": "wrong_password",
        }
        response = self.client.post(reverse("signin"), data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in response.data)


class SignoutViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="sahil@gmail.com",
            password="Password@123",
        )
        self.client.login(email="sahil@gmail.com", password="Password@123")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_signout_authenticated_user(self):
        response = self.client.get(reverse("signout"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], ["Logged out successfully."])

    def test_signout_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("signout"))
        self.assertEqual(response.status_code, 401)
