from django.db import models
from users.models import CustomUser


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("in_progress", "Подтверждено"),
        ("completed", "Выполнено"),
        ("cancelled", "Отменено"),
    ]
    SERVICE_CHOICES = [
        ("general_cleaning", "Общий клининг"),
        ("deep_cleaning", "Генеральная уборка"),
        ("post_construction", "Послестроительная уборка"),
        ("carpet_cleaning", "Химчистка ковров и мебели"),
    ]

    PAYMENT_CHOICES = [
        ("cash", "Наличные"),
        ("card", "Банковская карта"),
    ]
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="service_requests",
        verbose_name="Пользователь",
    )
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=18, verbose_name="Телефон")
    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        verbose_name="Вид услуги",
        blank=True,
        null=True,
    )
    other_service = models.TextField(blank=True, null=True, verbose_name="Иная услуга")
    preferred_datetime = models.DateTimeField(verbose_name="Желаемая дата и время")
    payment_method = models.CharField(
        max_length=4, choices=PAYMENT_CHOICES, verbose_name="Тип оплаты"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус заявки",
    )
    cancellation_reason = models.TextField(
        blank=True, null=True, verbose_name="Причина отмены"
    )

    def __str__(self):
        return f"Заявка от {self.user} на {self.preferred_datetime}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-preferred_datetime"]
