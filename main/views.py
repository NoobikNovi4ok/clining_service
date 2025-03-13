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
    lines = [
        "User-Agent: *",
        f"Sitemap: {settings.SITE_URL}/sitemap.xml",  # Убедитесь, что SITE_URL задан в settings.py
        "Disallow: /admin/",  # Запрет доступа к админке
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
