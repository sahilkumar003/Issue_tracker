from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.HomeAPIView.as_view(), name="home"),
    path("signin", views.SigninAPIView.as_view(), name="signin"),
    path("signup", views.SignupAPIView.as_view(), name="signup"),
    path("signout", views.SignoutAPIView.as_view(), name="signout"),
]
