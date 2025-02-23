from django.db import models
from users.models import CustomUser


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("NEW", "Новая заявка"),
        ("IN_PROGRESS", "В работе"),
        ("COMPLETED", "Выполнено"),
        ("CANCELLED", "Отменено"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15)
    service_type = models.CharField(max_length=255)
    custom_service = models.TextField(blank=True)
    preferred_payment = models.CharField(max_length=50)
    desired_date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    cancellation_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Заявка {self.id} от {self.user.username}"
