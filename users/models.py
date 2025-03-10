from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=50, blank=True, verbose_name="Отчество")
    phone = models.CharField(max_length=11, blank=False, verbose_name="Телефон")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")

    def __str__(self):
        return f"{self.username}"
