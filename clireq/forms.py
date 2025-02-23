from django import forms
from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = [
            "address",
            "contact_phone",
            "service_type",
            "custom_service",
            "preferred_payment",
            "desired_date_time",
        ]
