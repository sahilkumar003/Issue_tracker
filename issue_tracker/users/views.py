from django.views.generic import TemplateView
from users.models import User
from django.shortcuts import redirect
from django.contrib import messages
from users.serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_edit.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(email=self.request.user.email)
        serializer = UserSerializer(user)
        context["users"] = serializer.data
        return context

    def post(self, request):
        user = User.objects.get(email=request.user.email)
        serializer = UserSerializer(user, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Changes have been saved")
            return redirect("profile_edit")
        else:
            context = self.get_context_data(serializer_errors=serializer.errors)
            return self.render_to_response(context, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_view.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(email=self.request.user.email)
        serializer = UserSerializer(user)
        context["users"] = serializer.data
        return context
