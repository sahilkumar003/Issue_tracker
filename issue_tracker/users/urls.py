from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("profile_edit", views.profile_edit, name="profile_edit"),
]
