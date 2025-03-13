from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages, auth
from users.forms import RegistrationForm, UserLoginForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)  # Установка пароля
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(
        request, "users/register.html", {"form": form, "title": "Регистрация"}
    )


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home")
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"{user}, вы успешно вошли в аккаунт")
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context


class LogoutView(RedirectView):  # С выходом из аккаунта на главную страницу
    url = reverse_lazy("home")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "Успешный выход из аккаунта")
        return super().dispatch(request, *args, **kwargs)
