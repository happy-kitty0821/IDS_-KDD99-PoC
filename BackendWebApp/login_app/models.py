from django.db import models
from django.contrib.auth.models import User

class Admins(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    profilePic = models.ImageField(null=True, blank=True, upload_to="profile")

    def __str__(self):
        return self.name
