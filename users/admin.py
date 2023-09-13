from django.contrib import admin

from users.models import User

# Register your models here.
admin.site.site_header = "Issue Management System"


class UsersAdmin(admin.ModelAdmin):
    # fields = ["email", "first_name", "last_name"]
    list_display = ["id", "first_name", "last_name", "email", "password"]
    search_fields = ["first_name", "email"]
    list_filter = ["email"]
    list_editable = ["email"]


admin.site.register(User, UsersAdmin)
