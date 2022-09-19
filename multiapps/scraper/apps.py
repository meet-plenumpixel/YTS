"""
Configuration for specific scraper app
"""

# DJANGO LIBRARY
from django.apps import AppConfig



class ScraperConfig(AppConfig):
  """
  Config for scraper app
  """
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'scraper'

  def ready(self):
    # FIRSTPARTY LIBRARY
    import scraper.signals
