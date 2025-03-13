from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц, само доменное имя задается в админ-панели
    """

    protocol = "http"
    priority = 1
    changefreq = "weekly"

    def items(self):
        return ["home", "user:login", "user:register"]

    def location(self, item):
        return reverse(item)
