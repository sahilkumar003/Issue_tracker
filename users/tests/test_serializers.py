from datetime import date

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from users.models import User
from users.serializers import UserEditSerializer, UserSerializer


class UserSerializerTest(TestCase):
    def test_valid_user_data(self):
        data = {
            "email": "test@gmail.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "first_name": "sahil",
            "last_name": "kumar",
            "dob": "2000-01-01",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.create(serializer.validated_data)
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(str(user.dob), data["dob"])
        self.assertTrue(user.check_password(data["password"]))

    def test_validate_first_name_invalid(self):
        serializer = UserSerializer()
        invalid_value = "sahil123"
        with self.assertRaises(ValidationError) as context:
            serializer.validate_first_name(invalid_value)
        self.assertTrue("First Name should only contain alphabetical characters." in str(context.exception))

    def test_validate_last_name_invalid(self):
        serializer = UserSerializer()
        invalid_value = "kumar123"
        with self.assertRaises(ValidationError) as context:
            serializer.validate_last_name(invalid_value)
        self.assertTrue("Last Name should only contain alphabetical characters." in str(context.exception))

    def test_validate_dob_invalid(self):
        serializer = UserSerializer()
        invalid_value = date(2024, 5, 6)
        with self.assertRaises(ValidationError) as context:
            serializer.validate_dob(invalid_value)
        self.assertTrue("Date of birth cannot be in the future." in str(context.exception))

    def test_validate_email_invalid(self):
        serializer = UserSerializer()
        invalid_value = "test@example.com"
        with self.assertRaises(ValidationError) as context:
            serializer.validate_email(invalid_value)
        self.assertTrue("Only emails ending with @gmail.com are allowed." in str(context.exception))

    def test_validate_password_invalid(self):
        serializer = UserSerializer()
        invalid_value = "pass"
        with self.assertRaises(ValidationError) as context:
            serializer.validate_password(invalid_value)
        self.assertTrue(
            "Password must contain at least one lowercase letter, one uppercase letter, one number, one special character, and should be atleast 6 character long."
            in str(context.exception)
        )

    def test_validate_confirm_password_invalid(self):
        serializer = UserSerializer()
        serializer.initial_data = {"password": "Sahil@123"}
        invalid_value = "Kumar@123"
        with self.assertRaises(ValidationError) as context:
            serializer.validate_confirm_password(invalid_value)
        self.assertTrue("Passwords do not match." in str(context.exception))


class UserEditSerializerTest(TestCase):
    def test_update_valid(self):
        user = User.objects.create(
            email="test@gmail.com",
            first_name="sahil",
            last_name="kumar",
            password="Sahil@123",
            dob=date(1990, 1, 1),
        )
        serializer = UserEditSerializer(instance=user)
        data = {
            "first_name": "aman",
            "last_name": "kumar",
            "dob": date(1985, 6, 15),
        }
        updated_user = serializer.update(user, data)
        self.assertEqual(updated_user.first_name, data["first_name"])
        self.assertEqual(updated_user.last_name, data["last_name"])
        self.assertEqual(updated_user.dob, data["dob"])

    def test_update_email_and_password(self):
        user = User.objects.create(
            email="test@gmail.com",
            first_name="sahil",
            last_name="kumar",
            password="Sahil@123",
            dob=date(1990, 1, 1),
        )
        serializer = UserEditSerializer(instance=user)
        data = {
            "email": "newemail@gmail.com",
            "password": "NewSahil@123",
        }
        with self.assertRaises(ValidationError) as context:
            serializer.update(user, data)
        self.assertTrue("You cannot change your email or password." in str(context.exception))

    def test_update_invalid_dob(self):
        user = User.objects.create(
            email="test@gmail.com",
            first_name="sahil",
            last_name="kumar",
            password="Sahil@123",
            dob=date(1990, 1, 1),
        )
        serializer = UserEditSerializer(instance=user)
        invalid_data = {
            "dob": date(2024, 7, 5),
        }
        with self.assertRaises(ValidationError) as context:
            serializer.update(user, invalid_data)
        self.assertTrue("Date of birth cannot be in the future." in str(context.exception))

    def test_update_invalid_first_name(self):
        user = User.objects.create(
            email="test@gmail.com",
            first_name="sahil",
            last_name="kumar",
            password="Sahil@123",
            dob=date(1990, 1, 1),
        )
        serializer = UserEditSerializer(instance=user)
        invalid_data = {
            "first_name": "sahil12",
        }
        with self.assertRaises(ValidationError) as context:
            serializer.update(user, invalid_data)
        self.assertTrue("First Name should only contain alphabetical characters." in str(context.exception))

    def test_update_invalid_last_name(self):
        user = User.objects.create(
            email="test@gmail.com",
            first_name="sahil",
            last_name="kumar",
            password="Sahil@123",
            dob=date(1990, 1, 1),
        )
        serializer = UserEditSerializer(instance=user)
        invalid_data = {
            "last_name": "kumar12",
        }
        with self.assertRaises(ValidationError) as context:
            serializer.update(user, invalid_data)
        self.assertTrue("Last Name should only contain alphabetical characters." in str(context.exception))
