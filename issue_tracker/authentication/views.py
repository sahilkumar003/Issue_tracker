from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.token import RefreshToken


class IsLoggedIn(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
