from django.urls import path
from users.views import register, LogoutView, UserLoginView

app_name = "user"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
