from django.contrib import admin
from clireq.models import ServiceRequest


class ServiceRequestAdmin(admin.ModelAdmin):
    # Набор полей для формы редактирования
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "id",
                    "user",
                    "address",
                    "phone",
                    "service_type",
                    "other_service",
                    "preferred_datetime",
                    "payment_method",
                )
            },
        ),
        (
            "Статус заявки",
            {
                "fields": (
                    "status",
                    "cancellation_reason",
                )
            },
        ),
    )

    # Набор полей для формы создания
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "address",
                    "phone",
                    "service_type",
                    "other_service",
                    "preferred_datetime",
                    "payment_method",
                ),
            },
        ),
    )

    # Переопределение метода get_fieldsets для использования add_fieldsets при создании
    def get_fieldsets(self, request, obj=None):
        if not obj:  # Если объект еще не создан (режим добавления)
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    # Переопределение метода get_readonly_fields
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если объект уже существует (режим редактирования)
            # Делаем все поля, кроме status и cancellation_reason, доступными только для чтения
            return (
                "id",
                "user",
                "address",
                "phone",
                "service_type",
                "other_service",
                "preferred_datetime",
                "payment_method",
            )
        return ()  # При создании объекта все поля доступны для редактирования

        # Поля, которые будут отображаться в списке пользователей

    list_display = (
        "id",
        "user",
        "address",
        "phone",
        "service_type",
        "other_service",
        "preferred_datetime",
        "status",
        "cancellation_reason",
    )
    list_filter = ("status", "preferred_datetime")
    search_fields = ("user__full_name", "address")
    ordering = ("preferred_datetime",)
    filter_horizontal = ()

    def get_service_type(self, obj):
        return obj.get_service_type_display() if obj.service_type else obj.other_service

    get_service_type.short_description = "Услуга"

    def save_model(self, request, obj, form, change):
        if obj.status == "cancelled":
            if not obj.cancellation_reason:
                obj.cancellation_reason = "Причина не указана"
        else:
            # Если статус не "cancelled", очищаем причину отмены
            obj.cancellation_reason = None

        super().save_model(request, obj, form, change)


admin.site.register(ServiceRequest, ServiceRequestAdmin)
