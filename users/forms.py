import re
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "login",
                "name": "login",
                "placeholder": "Логин",
                "autocomplete": "username",
            }
        ),
        max_length=50,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Логин",
    )

    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "full_name",
                "name": "full_name",
                "placeholder": "ФИО",
                "autocomplete": "name",
            }
        ),
        max_length=255,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="ФИО",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "password",
                "name": "password",
                "placeholder": "Пароль",
                "autocomplete": "new-password",
            }
        ),
        strip=True,
        min_length=6,
        validators=[validate_password],
        label="Пароль",
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "confirm_password",
                "name": "confirm_password",
                "placeholder": "Подтвердите пароль",
                "autocomplete": "new-password",
            }
        ),
        strip=True,
        min_length=6,
        required=True,
        label="Подтверждение пароля",
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "phone",
                "name": "phone",
                "placeholder": "+7(XXX)-XXX-XX-XX",
                "autocomplete": "tel",
            }
        ),
        required=True,
        label="Номер телефона",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-2",
                "id": "email",
                "name": "email",
                "placeholder": "name@example.com",
                "autocomplete": "email",
            }
        ),
        required=True,
        label="Почта",
    )

    class Meta:
        model = CustomUser
        fields = [
            "login",
            "full_name",
            "password",
            "confirm_password",
            "phone",
            "email",
        ]

    def clean_login(self):
        login = self.cleaned_data.get("login")
        if CustomUser.objects.filter(login=login).exists():
            raise ValidationError("Логин уже занят.")
        return login

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        # Удаляем все символы, кроме цифр и "+"
        normalized_phone = re.sub(r"[^\d+]", "", phone)

        # Обработка различных форматов номера
        if len(normalized_phone) == 12 and normalized_phone.startswith("+7"):
            # Если номер начинается с +7 и имеет длину 12 символов, возвращаем его
            return normalized_phone[1:]  # Убираем "+" для сохранения только цифр
        elif len(normalized_phone) == 11 and normalized_phone.startswith("7"):
            # Если номер начинается с 7 и имеет длину 11 символов, возвращаем его
            return normalized_phone
        elif len(normalized_phone) == 11 and normalized_phone.startswith("8"):
            # Если номер начинается с 8, заменяем 8 на 7
            return "7" + normalized_phone[1:]
        else:
            raise ValidationError(
                "Неверный формат телефона. Используйте формат: +7(XXX)-XXX-XX-XX."
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Пароли не совпадают.")


from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    # Переопределяем поля username и password для кастомизации
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "autocomplete": "username",
                "placeholder": "Введите логин",
                "class": "form-control mb-2",
                "id": "username",
                "name": "username",
            }
        ),
        label="Логин",
    )
    password = forms.CharField(
        strip=True,  # Не удаляем пробелы из пароля
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Введите пароль",
                "class": "form-control mb-2",
                "id": "password",
                "name": "password",
            }
        ),
        label="Пароль",
    )

    error_messages = {
        "invalid_login": _(
            "Пожалуйста, введите правильный логин и пароль. "
            "Обратите внимание, что оба поля могут быть чувствительны к регистру."
        ),
        "inactive": _("Этот аккаунт неактивен."),
    }
