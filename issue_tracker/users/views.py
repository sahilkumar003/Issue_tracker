from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


class ProfileEditAPIView(APIView):
    def get(self, request):
        users = User.objects.get(email=request.user.email)
        context = {"users": users}
        return render(request, "users/profile_edit.html", context)

    def post(self, request):
        data = User.objects.get(email=request.user.email)
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        user = User.objects.get(email=request.user.email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "Changes have been saved")
        return redirect("profile_edit")
