from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("project_create/", views.CreateProjectView.as_view(), name="project_create"),
]
