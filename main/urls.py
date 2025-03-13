from django.urls import path
from main.views import HomePageView, robots_txt

from django.contrib.sitemaps.views import sitemap
from main.sitemap import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", robots_txt, name="robots"),
]
