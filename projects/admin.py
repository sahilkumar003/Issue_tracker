from django.contrib import admin

from projects.models import Member, Project

# Register your models here.
admin.site.site_header = "Issue Management System"


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "created_at", "updated_at"]
    search_fields = ["title"]
    list_filter = ["title"]


class MemberAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "project", "role"]
    search_fields = ["user", "project", "role"]
    list_filter = ["role"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Member, MemberAdmin)
