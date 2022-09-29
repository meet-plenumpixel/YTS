"""
ScraperApp URL Configuration
"""

# DJANGO LIBRARY
from django.urls import path, re_path

# FIRSTPARTY LIBRARY
from scraper import views as scraper_views



urlpatterns = [
  path("", scraper_views.HomeTemplateView.as_view(), name="home"),
  path("results", scraper_views.SearchRedirectView.as_view(), name="search-query"),
  path("watch", scraper_views.WatchTemplateView.as_view(), name="watch-video"),
  re_path(
    r"^(?P<c_type>(u|c|user|channel))/(?P<c_url>([%\w\d_\-]+))(/videos|/featured)?$",
    scraper_views.VideoTemplateView.as_view(),
    name="channel",
  ),
]
