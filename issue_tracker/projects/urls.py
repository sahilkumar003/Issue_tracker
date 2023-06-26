from django.urls import path
from . import views

urlpatterns = [
    path("project_create/", views.CreateProjectView.as_view(), name="project_create"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/<str:filter_param>/",
        views.DashboardView.as_view(),
        name="dashboard_filter",
    ),
]
