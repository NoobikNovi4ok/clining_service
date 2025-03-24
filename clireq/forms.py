import re
from django import forms
from django.core.exceptions import ValidationError
from .models import ServiceRequest
from datetime import datetime, timedelta


class ServiceRequestForm(forms.ModelForm):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "+7(XXX)-XXX-XX-XX",
                "class": "form-control mb-2",
                "id": "id_phone",
            }
        ),
        label="Номер телефона",
    )
    other_service = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control mb-2",
                "id": "id_other_service",
                "style": "display: none;",  # Скрываем поле по умолчанию
            }
        ),
        required=False,
        label="Описание иной услуги",
    )
    is_other_service = forms.BooleanField(
        required=False,
        label="Иная услуга",
        widget=forms.CheckboxInput(attrs={"id": "id_is_other_service"}),
    )

    class Meta:
        model = ServiceRequest
        fields = [
            "address",
            "phone",
            "service_type",
            "other_service",
            "preferred_datetime",
            "payment_method",
        ]
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "class": "form-control mb-2",
                    "placeholder": "Введите адрес",
                    "id": "id_address",
                }
            ),
            "service_type": forms.Select(
                attrs={"class": "form-control mb-2", "id": "id_service_type"}
            ),
            "preferred_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control mb-2",
                    "id": "id_preferred_datetime",
                }
            ),
            "payment_method": forms.RadioSelect(attrs={"class": "form-check-input"}),
        }
        labels = {
            "address": "Адрес",
            "service_type": "Вид услуги",
            "preferred_datetime": "Желаемая дата и время",
            "payment_method": "Тип оплаты",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем пустой выбор для payment_method
        self.fields["payment_method"].choices = [
            ("cash", "Наличные"),
            ("card", "Банковская карта"),
        ]
        self.fields["payment_method"].initial = "cash"  # Начальное значение
        now = datetime.now()
        self.fields["preferred_datetime"].widget.attrs.update(
            {
                "min": (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M"),
                "max": (now + timedelta(days=31)).strftime("%Y-%m-%dT%H:%M"),
            }
        )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        # Удаляем все символы, кроме цифр
        normalized_phone = re.sub(r"[^\d]", "", phone)

        # Проверяем формат номера
        if len(normalized_phone) == 11 and normalized_phone.startswith("7"):
            return normalized_phone
        elif len(normalized_phone) == 11 and normalized_phone.startswith("8"):
            return normalized_phone
        else:
            raise ValidationError(
                "Неверный формат телефона. Используйте формат: +7(XXX)-XXX-XX-XX."
            )

    def clean_preferred_datetime(self):
        selected_datetime = self.cleaned_data["preferred_datetime"]
        # Удаляем временную зону, если она есть

        if selected_datetime and selected_datetime.tzinfo:
            selected_datetime = selected_datetime.replace(tzinfo=None)

        if selected_datetime < datetime.now():
            raise forms.ValidationError("Дата и время не могут быть в прошлом.")
        return selected_datetime

    def clean(self):
        cleaned_data = super().clean()
        is_other_service = cleaned_data.get("is_other_service")
        service_type = cleaned_data.get("service_type")
        other_service = cleaned_data.get("other_service")

        # Если выбран чекбокс "Иная услуга", поле "other_service" должно быть заполнено
        if is_other_service and not other_service:
            raise ValidationError("Пожалуйста, опишите иную услугу.")
        elif not is_other_service and not service_type:
            raise ValidationError("Выберите вид услуги или отметьте 'Иная услуга'.")

        return cleaned_data
