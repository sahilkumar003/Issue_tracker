from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.serializers import UserSerializer
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


class HomeView(TemplateView):
    template_name = "authentication/index.html"


class SignupView(TemplateView):
    template_name = "authentication/signup.html"

    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "Your account has been successfully created")
            subject = "Welcome to the Issue Tracker System"
            message = f"Hi {user.first_name}, thank you for registering in Issue Tracker System"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect("signin")
        else:
            context = self.get_context_data(serializer_errors=serializer.errors)
            return self.render_to_response(context, status=status.HTTP_400_BAD_REQUEST)


class SigninView(TemplateView):
    template_name = "authentication/signin.html"

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("projects:dashboard")
        else:
            messages.error(request, "Bad credentials")
            return redirect("signin")


class SignoutView(TemplateView):
    template_name = "authentication/index.html"

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("home")
