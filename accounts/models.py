from django.db import models

from django.contrib.auth.models import AbstractUser 
from .manager import *

class CustomUser(AbstractUser):
    username = None
    email=models.EmailField(unique=True)
    Phone_number = models.CharField(max_length=12,null=True)
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

