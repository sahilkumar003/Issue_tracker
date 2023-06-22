from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("profile_edit", views.ProfileEditAPIView.as_view(), name="profile_edit"),
]
