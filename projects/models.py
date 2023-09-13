from django.db import models

from users.models import User


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
    members = models.ManyToManyField(User, through="Member")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Member(models.Model):
    ROLE_CHOICES = (
        (1, "Project Manager"),
        (2, "Project Member"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.project.title}"
