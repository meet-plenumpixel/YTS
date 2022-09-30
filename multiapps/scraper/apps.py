"""
Configuration for specific scraper app
"""

# STDLIB LIBRARY
import logging
import os

# DJANGO LIBRARY
from django.apps import AppConfig
from django.db.utils import OperationalError



# from django.core.management import call_command

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
    logger.info('scraper is now ready')
