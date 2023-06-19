from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.serializers import UserSerializer


class HomeAPIView(APIView):
    def get(self, request):
        return render(request, "authentication/index.html")


class SignupAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Your account has been successfully created")
            return redirect("signin")
        return Response(serializer.errors, status=404)

    def get(self, request):
        return render(request, "authentication/signup.html")


class SigninAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            print(email, password, request.POST)
            login(request, user)
            request.session["first_name"] = user.first_name
            return redirect("home")
        else:
            messages.error(request, "Bad credentials")
            return redirect("signin")

    def get(self, request):
        return render(request, "authentication/signin.html")


class SignoutAPIView(APIView):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("home")


def home(request):
    return render(request, "dashboard/home.html")
