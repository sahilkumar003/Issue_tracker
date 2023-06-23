import re
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "dob"]

    def validate_first_name(self, value):
        name_regex = re.compile(r"^[A-Za-z]+$")
        if not name_regex.match(value):
            raise serializers.ValidationError(
                "Name should only contain alphabetical characters."
            )
        return value

    def validate_last_name(self, value):
        name_regex = re.compile(r"^[A-Za-z]+$")
        if not name_regex.match(value):
            raise serializers.ValidationError(
                "Name should only contain alphabetical characters."
            )
        return value

    def validate_email(self, value):
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError(
                "Only emails ending with @gmail.com are allowed."
            )
        return value

    def validate_password(self, value):
        password_regex = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
        )
        if not password_regex.match(value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter, one uppercase letter, one number, one special character, and should be atleast 6 character long"
            )
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
