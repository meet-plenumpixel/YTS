"""
Django settings for production environment
"""
# STDLIB LIBRARY
import os

# LOCALFOLDER LIBRARY
from . import LOGGING



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

__all__ = [i for i in dir() if i.isupper()]    # type: ignore
