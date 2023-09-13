from django.contrib import admin

from stories.models import Story

# Register your models here.
admin.site.site_header = "Issue Management System"


class StoriesAdmin(admin.ModelAdmin):
    # fields = ["email", "first_name", "last_name"]
    list_display = [
        "id",
        "title",
        "description",
        "assignee",
        "estimate",
        "project",
        "status",
        "is_scheduled",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "title",
        "description",
        "assignee",
        "estimate",
        "project",
        "status",
        "is_scheduled",
        "created_at",
        "updated_at",
    ]


admin.site.register(Story, StoriesAdmin)
