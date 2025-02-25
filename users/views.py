from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import RedirectView
from .forms import RegistrationForm, UserLoginForm
from django.contrib import messages, auth
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Успешный вход в аккаунт")
            return redirect("home")
        else:
            return render(
                request, "users/login.html", {"error": "Неверный логин или пароль"}
            )
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


class LogoutView(RedirectView):  # С выходом из аккаунта на главную страницу
    url = reverse_lazy("home")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "Успешный выход из аккаунта")
        return super().dispatch(request, *args, **kwargs)
