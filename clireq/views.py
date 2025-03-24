from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .forms import ServiceRequestForm
from .models import ServiceRequest


@login_required
def create_request(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Привязываем заявку к пользователю
            service_request.save()
            messages.success(request, "Успешное создание заявки")
            return redirect("clireq:request_history")
    else:
        form = ServiceRequestForm()
    return render(
        request,
        "clireq/create_request.html",
        {
            "form": form,
            "title": "Формирование заявки",
            "meta_description": (
                "Исправьте ошибки в форме, чтобы успешно создать заявку."
                if form.errors
                else "Создайте новую заявку на сайте. Укажите адрес, контактные данные, тип услуги и предпочтительное время для обработки вашего запроса."
            ),
            "meta_keywords": "создание заявки, форма заявки, отправка заявки, выбор услуги, контактные данные, предпочтительное время",
        },
    )


@login_required
def request_history(request):
    requests = ServiceRequest.objects.filter(user=request.user)
    return render(
        request,
        "clireq/request_history.html",
        {
            "requests": requests,
            "title": "Создание заявки",
            "meta_description": "Просмотрите историю ваших заявок на сайте. Здесь вы найдете информацию о статусе заявок, услугах и деталях оплаты.",
            "meta_keywords": "история заявок, статус заявки, услуги, оплата, отмена заявки, создание заявки",
        },
    )
