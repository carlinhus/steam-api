from django.db import models
from django.contrib.auth import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        on_delete=models.CASCADE,
    )
    steamURL = models.CharField(max_length=255)
    joined_at = models.DateTimeField(auto_now=True)