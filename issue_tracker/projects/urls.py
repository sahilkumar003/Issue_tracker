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
    path(
        "project_edit/<int:project_id>/",
        views.ProjectEditView.as_view(),
        name="project_edit",
    ),
    path(
        "project_delete/<int:project_id>/",
        views.ProjectDeleteView.as_view(),
        name="project_delete",
    ),
]
