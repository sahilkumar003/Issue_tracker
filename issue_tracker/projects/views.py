from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import Project, Member
from users.models import User
from django import forms


class ProjectCreateView(CreateView):
    model = Project
    fields = ["title", "description", "members"]

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        if request is not None:
            self.members = forms.ModelMultipleChoiceField(
                queryset=User.objects.exclude(
                    projects__in=Project.objects.filter(creator=request.user)
                ),
                widget=forms.CheckboxSelectMultiple,
            )

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return redirect("projects:project_create")
