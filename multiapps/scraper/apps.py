"""
Configuration for specific scraper app
"""

# STDLIB LIBRARY
import logging
import os

# DJANGO LIBRARY
from django.apps import AppConfig



logger = logging.getLogger(__name__)


class ScraperConfig(AppConfig):
  """
  Config for scraper app
  """
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'scraper'

  def ready(self):
    # FIRSTPARTY LIBRARY
    import scraper.signals
    from scraper.models import Setting

    for key,value in Setting.objects.values_list("key", "value"):
      os.environ[key] = value
      logger.debug(f'SET {key}="{value}"')
