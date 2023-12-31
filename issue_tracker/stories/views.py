from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from .models import Story
from projects.models import Project
from django.contrib import messages
from .serializers import StorySerializer
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.conf import settings
from django.core.mail import send_mail


class CreateStoryView(LoginRequiredMixin, TemplateView):
    template_name = "stories/stories_create.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        project = Project.objects.get(id=project_id)
        if (
            self.request.user in project.members.all()
            or self.request.user == project.owner
        ):
            users = list(project.members.all())
            users.append(project.owner)
        else:
            users = None

        context["project"] = project
        context["users"] = users
        return context

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "assignee": request.POST.get("assignee"),
            "estimate": request.POST.get("estimate"),
            "project": project_id,
        }
        serializer = StorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Story has been successfully created")
            assignee_id = request.POST.get("assignee")
            assignee = User.objects.get(id=assignee_id)
            subject = "You have been assigned a story"
            message = f"You have been assigned with the story '{serializer.data['title']}' in project '{project.title}'."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [assignee.email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect("projects:dashboard")

        else:
            print(serializer.errors)
            context = self.get_context_data(serializer_errors=serializer.errors)
            return self.render_to_response(context)


class StoryListView(LoginRequiredMixin, TemplateView):
    template_name = "stories/stories_list.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        project = Project.objects.get(id=project_id)
        scheduled_stories = Story.objects.filter(
            project=project, is_scheduled=1, is_deleted=False
        ).order_by("-status", "created_at")
        unscheduled_stories = Story.objects.filter(
            project=project, is_scheduled=2, is_deleted=False
        ).order_by("-status", "created_at")
        context["project"] = project
        context["scheduled_stories"] = scheduled_stories
        context["unscheduled_stories"] = unscheduled_stories
        return context


class UpdateStoryView(LoginRequiredMixin, TemplateView):
    template_name = "stories/stories_update.html"
    login_url = "signin"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs["project_id"]
        story_id = self.kwargs["story_id"]
        project = Project.objects.get(id=project_id)
        story = Story.objects.get(id=story_id, project_id=project_id)

        if (
            self.request.user in project.members.all()
            or self.request.user == project.owner
        ):
            users = list(project.members.all())
            users.append(project.owner)
        else:
            users = None

        context["project"] = project
        context["story"] = story
        context["users"] = users
        context["status_choices"] = Story.STATUS_CHOICES
        context["schedule_choices"] = Story.SCHEDULE_CHOICES
        return context

    def post(self, request, project_id, story_id):
        story = Story.objects.get(id=story_id)

        if story.status == 4:
            messages.error(request, "Delivered stories cannot be updated.")
            return self.get(request, project_id=project_id, story_id=story_id)

        if story.status in [2, 3] and request.POST.get("is_scheduled") == "2":
            messages.error(request, "Started/Finished stories cannot be unscheduled.")
            return self.get(request, project_id=project_id, story_id=story_id)

        if story.status in [2, 3] and request.POST.get("assignee") != str(
            story.assignee.id
        ):
            messages.error(
                request,
                "Assignee cannot be changed for stories with status finished or started.",
            )
            return self.get(request, project_id=project_id, story_id=story_id)


        serializer = StorySerializer(story, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Story has been updated successfully")
            return redirect("stories:stories_list", project_id=project_id)
        else:
            context = self.get_context_data()
            context["serializer_errors"] = serializer.errors
            return self.render_to_response(context)


class StoryDeleteView(LoginRequiredMixin, View):
    def post(self, request, project_id, story_id):
        story = Story.objects.get(id=story_id)
        story.is_deleted = True
        story.save()

        messages.success(request, "Story has been soft deleted")
        return redirect("stories:stories_list", project_id=project_id)
