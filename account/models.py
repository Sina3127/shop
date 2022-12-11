from django.contrib.auth.models import AbstractUser
from django.db import models


class Avatar(models.Model):
    image = models.ImageField(upload_to='uploads/')


class CustomUser(AbstractUser):
    avatar = models.ForeignKey(Avatar, on_delete=models.PROTECT, null=True)


    def save(self, *args, **kwargs):
        if self.avatar is None:
            self.avatar = Avatar.objects.first()

        super(CustomUser, self).save(*args, **kwargs)

class Address(models.Model):
    address = models.TextField(max_length=225)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="address")

    def __str__(self):
        return self.user.username + "  " + self.address
