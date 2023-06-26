from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("profile_edit", views.ProfileEditView.as_view(), name="profile_edit"),
    path("profile_view", views.ProfileView.as_view(), name="profile_view"),
]
