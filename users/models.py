import re
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def normalize_phone(self, phone):
        """
        Нормализует телефонный номер:
        - Удаляет все символы, кроме цифр и знака '+'.
        - Приводит номер к формату +7XXXXXXXXXX.
        """
        # Очищаем номер от всех символов, кроме цифр и '+'
        cleaned_phone = re.sub(r"[^\d]", "", phone)

        # Проверяем, начинается ли номер с '+7' или '8'
        if cleaned_phone.startswith("7") or cleaned_phone.startswith("8"):
            normalized_phone = cleaned_phone
        else:
            raise ValueError(
                "Некорректный формат телефона. Номер должен начинаться с '+7' или '8'."
            )

        # Проверяем длину номера
        if len(normalized_phone) != 11:
            raise ValueError(
                "Некорректная длина номера. Номер должен содержать 10 цифр после кода страны."
            )

        return normalized_phone

    def create_user(self, login, email, phone, password=None, **extra_fields):
        if not login:
            raise ValueError("Логин обязателен")
        if not email:
            raise ValueError("Email обязателен")
        if not phone:
            raise ValueError("Телефон обязателен")

        email = self.normalize_email(email)
        phone = self.normalize_phone(phone)
        user = self.model(login=login, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(login, email, phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Валидатор для кириллических символов
    cyrillic_validator = RegexValidator(
        regex=r"^[а-яА-ЯёЁ\s\-]+$",
        message="ФИО должно содержать только кириллические символы, пробелы и дефисы.",
    )

    login = models.CharField(max_length=50, unique=True, verbose_name="Логин")
    full_name = models.CharField(
        max_length=255, validators=[cyrillic_validator], verbose_name="ФИО"
    )
    phone = models.CharField(
        max_length=25, blank=False, null=False, verbose_name="Телефон"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")

    objects = CustomUserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["email", "phone", "full_name"]

    @property
    def is_superuser(self):
        return self.is_admin

    def __str__(self):
        return f"{self.login} ({self.full_name})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["login"]
        db_table = "Пользователи"
