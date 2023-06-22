from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import Project, Member
from users.models import User
from django.contrib import messages


class CreateProjectView(TemplateView):
    template_name = "projects/project_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        context["users"] = users
        return context

    def post(self, request):
        print(request.POST)
        title = request.POST.get("title")
        description = request.POST.get("description")
        owner = request.POST.get("owner") == "on"
        members = request.POST.getlist("members")

        project = Project.objects.create(
            title=title, description=description, owner=owner
        )
        for member_id in members:
            user = User.objects.get(id=member_id)
            role = request.POST.get(f"member_role_{member_id}")
            Member.objects.create(user=user, project=project, role=role)

        messages.success(request, "Project has been successfully created")
        return redirect("home")
