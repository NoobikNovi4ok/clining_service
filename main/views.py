from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings


class HomePageView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


def robots_txt(request):
    admin_url = reverse("admin:index")
    create_url = reverse("clireq:create_request")
    history_url = reverse("clireq:request_history")
    lines = [
        "User-Agent: *",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",  # Убедитесь, что SITE_URL задан в settings.py
        f"Disallow: {admin_url}",  # Запрет доступа к админке
        f"Disallow: {create_url}",  # Запрет доступа к созданию заявок
        f"Disallow: {history_url}",  # Запрет доступа к истории заявок
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
