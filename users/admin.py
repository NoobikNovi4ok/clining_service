from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Определение полей для отображения в интерфейсе администратора
    fieldsets = (
        # Основная информация
        (None, {"fields": ("login", "password")}),
        # Персональные данные
        (
            _("Персональные данные"),
            {
                "fields": (
                    "full_name",
                    "phone",
                    "email",
                )
            },
        ),
        # Права доступа
        (
            _("Права"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_staff",
                )
            },
        ),
    )

    # Определение полей для формы добавления нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "login",
                    "email",
                    "full_name",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    # Поля, которые будут отображаться в списке пользователей
    list_display = (
        "login",
        "email",
        "full_name",
        "phone",
        "is_active",
        "is_admin",
        "is_staff",
    )

    # Поля, по которым можно выполнять поиск
    search_fields = (
        "login",
        "email",
        "full_name",
        "phone",
    )

    # Поля, которые можно использовать для фильтрации
    list_filter = (
        "is_active",
        "is_admin",
        "is_staff",
    )

    # Поля, которые можно редактировать непосредственно из списка
    list_editable = (
        "is_active",
        "is_admin",
        "is_staff",
    )

    # Поле, которое используется как ссылка на страницу редактирования
    ordering = ("login",)


# Регистрация модели CustomUser с настроенным интерфейсом администратора
admin.site.register(CustomUser, CustomUserAdmin)
