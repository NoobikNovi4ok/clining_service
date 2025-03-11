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
            return redirect("clireq:request_history")
    else:
        form = ServiceRequestForm()
    return render(request, "clireq/create_request.html", {"form": form})


@login_required
def request_history(request):
    requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, "clireq/request_history.html", {"requests": requests})
