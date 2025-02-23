from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("req/", include("clireq.urls")),
    path("user/", include("users.urls", namespace="user")),
    path("", include("main.urls")),
]
