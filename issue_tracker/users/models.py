from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
import datetime

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
