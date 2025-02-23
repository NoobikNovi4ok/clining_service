from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=False)
    address = models.CharField(max_length=255, blank=True)
