from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
import re


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "username",
                "name": "username",
                "placeholder": "Login",
                "autocomplete": "Login",
            }
        ),
        max_length=50,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Логин",
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "name",
                "name": "name",
                "placeholder": "Name",
                "autocomplete": "Name",
            }
        ),
        max_length=50,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Имя",
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "surname",
                "name": "surname",
                "placeholder": "Lastname",
                "autocomplete": "Lastname",
            }
        ),
        max_length=50,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Фамилия",
    )

    patronymic = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "patronymic",
                "name": "patronymic",
                "placeholder": "Patronymic",
                "autocomplete": "Patronymic",
            }
        ),
        max_length=50,
        required=False,
        label="Отчество",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "password",
                "name": "Password",
                "placeholder": "Password",
                "autocomplete": "Password",
            }
        ),
        min_length=6,
        validators=[validate_password],
        label="Пароль",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "confirm_password",
                "name": "Confirm_password",
                "placeholder": "Confirm_password",
                "autocomplete": "Confirm_password",
            }
        ),
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
                "autocomplete": "+7(XXX)-XXX-XX-XX",
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
                "autocomplete": "example@gmail.com",
            }
        ),
        required=True,
        label="Почта",
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "patronymic",
            "password",
            "confirm_password",
            "phone",
            "email",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Логин"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Фамилия"}),
            "patronymic": forms.TextInput(attrs={"placeholder": "Отчество"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7(XXX)-XXX-XX-XX"}),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Логин уже занят.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        # Удаляем все символы, кроме цифр и "+"
        normalized_phone = re.sub(r"[^\d+]", "", phone)

        # Обработка различных форматов номера
        if len(normalized_phone) == 11:
            if normalized_phone.startswith("7") or normalized_phone.startswith("8"):
                return normalized_phone
            raise ValidationError("Неверный формат телефона. Используйте 7XXXXXXXXXX.")
        raise ValidationError("Неверный формат телефона. Используйте 7XXXXXXXXXX.")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Пароли не совпадают")
