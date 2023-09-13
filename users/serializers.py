import re
from datetime import date

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "dob",
            "confirm_password",
        ]

    def validate_first_name(self, value):
        name_regex = re.compile(r"^[A-Za-z]+$")
        if not name_regex.match(value):
            raise serializers.ValidationError(
                {"first_name": ["First Name should only contain alphabetical characters."]}
            )
        return value

    def validate_last_name(self, value):
        name_regex = re.compile(r"^[A-Za-z]+$")
        if not name_regex.match(value):
            raise serializers.ValidationError({"last_name": ["Last Name should only contain alphabetical characters."]})
        return value

    def validate_dob(self, value):
        if value > date.today():
            raise serializers.ValidationError({"dob": ["Date of birth cannot be in the future."]})
        return value

    def validate_email(self, value):
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError({"email": ["Only emails ending with @gmail.com are allowed."]})
        return value

    def validate_password(self, value):
        password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$")
        if not password_regex.match(value):
            raise serializers.ValidationError(
                {
                    "password": [
                        "Password must contain at least one lowercase letter, one uppercase letter, one number, one special character, and should be atleast 6 character long."
                    ]
                }
            )
        return value

    def validate_confirm_password(self, value):
        if value != self.initial_data.get("password"):
            raise serializers.ValidationError({"confirm_password": ["Passwords do not match."]})
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            dob=validated_data["dob"],
        )
        return user


class UserEditSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "dob", "email", "password"]

    def validate_first_name(self, value):
        name_regex = re.compile(r"^[A-Za-z]+$")
        if not name_regex.match(value):
            raise serializers.ValidationError(
                {"first_name": ["First Name should only contain alphabetical characters."]}
            )
        return value

    def validate_last_name(self, value):
        name_regex = re.compile(r"^[A-Za-z]+$")
        if not name_regex.match(value):
            raise serializers.ValidationError({"last_name": ["Last Name should only contain alphabetical characters."]})
        return value

    def validate_dob(self, value):
        if value > date.today():
            raise serializers.ValidationError({"dob": ["Date of birth cannot be in the future."]})
        return value

    def update(self, instance, validated_data):
        if "email" in validated_data or "password" in validated_data:
            raise serializers.ValidationError({"email_Password": ["You cannot change your email or password."]})

        instance.first_name = self.validate_first_name(validated_data.get("first_name", instance.first_name))
        instance.last_name = self.validate_last_name(validated_data.get("last_name", instance.last_name))
        instance.dob = self.validate_dob(validated_data.get("dob", instance.dob))

        instance.save()
        return instance
