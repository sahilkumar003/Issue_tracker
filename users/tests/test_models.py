from django.test import TestCase

from users.models import User


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        email = "test@example.com"
        password = "testpassword"
        first_name = "Test"
        last_name = "User"
        dob = "2001-08-07"
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
        )
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.dob, dob)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        email = "admin@example.com"
        password = "adminpassword"
        admin_user = User.objects.create_superuser(email=email, password=password)
        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.check_password(password))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_user_missing_email(self):
        password = "testpassword"
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password=password,
                first_name="Test",
                last_name="User",
                dob="2001-08-07",
            )

    def test_create_superuser_not_staff(self):
        email = "admin@example.com"
        password = "adminpassword"
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=email,
                password=password,
                is_staff=False,
                is_superuser=True,
            )

    def test_create_superuser_not_superuser(self):
        email = "admin@example.com"
        password = "adminpassword"
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=email,
                password=password,
                is_staff=True,
                is_superuser=False,
            )

    def test_str_representation(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            first_name="test",
            last_name="user",
            dob="2000-07-08",
        )
        expected_str = "test user"
        self.assertEqual(str(user), expected_str)
