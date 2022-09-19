"""
Django settings for production environment
"""
# STDLIB LIBRARY
import os

# THIRDPARTY LIBRARY
import dj_database_url

# LOCALFOLDER LIBRARY
from . import DATABASES, LOGGING, MIDDLEWARE, STATICFILES_STORAGE



# add WhiteNoiseMiddleware
MIDDLEWARE.insert(
  MIDDLEWARE.index(
    'django.middleware.security.SecurityMiddleware'
  )+1,
  'whitenoise.middleware.WhiteNoiseMiddleware',
)


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# set logger for logging module
LOGGING['loggers'].update({
  'scraper': {
    'handlers': ['console', 'file'],
    'level': 'INFO',
    'propagate': True,
  },
  '': {
    'handlers': ['console', 'file'],
    'level': 'INFO',
    'propagate': True,
  },
})

DATABASES['default'].update(dj_database_url.config(conn_max_age=600))

__all__ = [i for i in dir() if i.isupper()]    # type: ignore
