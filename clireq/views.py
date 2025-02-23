from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .forms import ServiceRequestForm
from .models import ServiceRequest


@login_required
def create_request(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            return redirect("request_history")
    else:
        form = ServiceRequestForm()
    return render(request, "main/create_request.html", {"form": form})


@login_required
def request_history(request):
    requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, "main/request_history.html", {"requests": requests})
