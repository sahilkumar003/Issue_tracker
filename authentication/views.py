from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer


class IsLoggedIn(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class SignupView(APIView):
    permission_classes = [IsLoggedIn]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Your account has been successfully created")
            subject = "Welcome to the Issue Tracker System"
            message = f"Hi {user.first_name}, thank you for registering in the Issue Tracker System"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response(
                {
                    "message": ["Account has been successfully created."],
                    "access_token": access_token,
                }
            )
        else:
            return Response(serializer.errors, status=400)


class SigninView(APIView):
    permission_classes = [IsLoggedIn]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response(
                {
                    "message": ["Logged in successfully."],
                    "access_token": access_token,
                }
            )
        else:
            return Response({"error": ["Bad credentials."]}, status=400)


class SignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({"message": ["Logged out successfully."]})
