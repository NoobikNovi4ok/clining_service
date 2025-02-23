from django.urls import path
from clireq.views import create_request, request_history

urlpatterns = [
    path("create-request/", create_request, name="create_request"),
    path("request-history/", request_history, name="request_history"),
]
