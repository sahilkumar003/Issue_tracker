from django.db import models

from projects.models import Project
from users.models import User


class Story(models.Model):
    STATUS_CHOICES = (
        (1, "Not Started"),
        (2, "Started"),
        (3, "Finished"),
        (4, "Delivered"),
    )

    SCHEDULE_CHOICES = (
        (1, "Scheduled"),
        (2, "Not Scheduled"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estimate = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    is_scheduled = models.IntegerField(choices=SCHEDULE_CHOICES, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title
