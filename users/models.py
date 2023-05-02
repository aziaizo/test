from django.contrib.auth.models import AbstractUser
from django.db import models
from .models import AbstractUser


class UserModel(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=150)

class Confirm(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=10)


class Image(models.Model):
    image = models.ImageField(upload_to='media')
