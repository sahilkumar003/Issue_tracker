from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("project-create/", views.ProjectCreateView.as_view(), name="project_create"),
]
