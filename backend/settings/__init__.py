"""
This module helps to manage environment settings.
"""

# STDLIB LIBRARY
import logging

# LOCALFOLDER LIBRARY
from ._base import *



logger = logging.getLogger(__name__)


try:
  # LOCALFOLDER LIBRARY
  from .prod import *
  logger.info('production settings imported')

except  ImportError or ModuleNotFoundError as e:
  logger.error('production settings not available')


try:
  # LOCALFOLDER LIBRARY
  from .local import *
  logger.info('development settings imported')

except ImportError or ModuleNotFoundError as e:
  logger.warning('local settings not available')



# # environment settings
# if DEBUG:  # type: ignore
#     try:
#         # LOCALFOLDER LIBRARY
#         from .local import *
#     # pylint: disable-next=:binary-op-exception
#     except ImportError or ModuleNotFoundError:
#         pass
# else:
#     # LOCALFOLDER LIBRARY
#     from .prod import *
