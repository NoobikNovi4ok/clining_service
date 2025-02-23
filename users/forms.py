from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Логин уже занят")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 6:
            raise forms.ValidationError("Пароль должен содержать минимум 6 символов")
        return password


class UserLoginForm(AuthenticationForm):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "login",
                "name": "login",
                "placeholder": "Логин",
            }
        ),
        max_length=40,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Логин",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "password",
                "name": "Password",
                "placeholder": "Пароль",
            }
        ),
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Пароль",
    )

    error_messages = {
        "invalid_login": "Неверный логин или пароль. Пожалуйста, попробуйте снова."
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = self.fields.pop("login")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = self.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def authenticate(self, username=None, password=None):
        try:
            user = CustomUser.objects.get(login=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
