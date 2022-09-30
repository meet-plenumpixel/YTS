"""
Configuration for specific scraper app
"""

# STDLIB LIBRARY
import logging
import os

# DJANGO LIBRARY
from django.apps import AppConfig



# from django.db.utils import OperationalError
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
    from scraper.models import Setting
    
    try:
      for key,value in Setting.objects.values_list("key", "value"):
        os.environ[key] = value
        logger.debug(f'SET {key}="{value}"')
    except Exception as e:
      logger.error('app level setting not imported from setting model')
      # call_command('makemigrations')
      # call_command('migrate')

