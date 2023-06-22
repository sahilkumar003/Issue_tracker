from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("signin", views.SigninView.as_view(), name="signin"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("signout", views.SignoutView.as_view(), name="signout"),
]
