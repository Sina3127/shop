from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

class Address(models.Model):
    address = models.TextField(max_length=225)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="address")
    def __str__(self):
        return self.user.username + "  " + self.address