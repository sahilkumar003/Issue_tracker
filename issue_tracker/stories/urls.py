from django.urls import path
from . import views

urlpatterns = [
    path(
        "create/<int:project_id>/",
        views.CreateStoryView.as_view(),
        name="stories_create",
    ),
    path("list/<int:project_id>/", views.StoryListView.as_view(), name="stories_list"),
    path(
        "update/<int:project_id>/<int:story_id>/",
        views.UpdateStoryView.as_view(),
        name="stories_update",
    ),
    path(
        "delete/<int:project_id>/<int:story_id>/",
        views.StoryDeleteView.as_view(),
        name="stories_delete",
    ),
]
