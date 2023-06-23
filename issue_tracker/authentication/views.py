from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.serializers import UserSerializer
from rest_framework import status


class HomeView(TemplateView):
    template_name = "authentication/index.html"


class SignupView(TemplateView):
    template_name = "authentication/signup.html"

    def post(self, request):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Your account has been successfully created")
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
            return redirect("home")
        else:
            messages.error(request, "Bad credentials")
            return redirect("signin")


class SignoutView(TemplateView):
    template_name = "authentication/index.html"

    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("home")
