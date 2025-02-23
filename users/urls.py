from django.urls import path
from users.views import register, user_login, LogoutView

app_name = "user"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
