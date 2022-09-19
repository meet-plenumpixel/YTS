"""
This module helps to manage environment settings.
"""

# import only ENV variables (uppercase variable)
from ._base import *  # isort: skip


# environment settings
if DEBUG:  # type: ignore
    try:
        # LOCALFOLDER LIBRARY
        from .local import *
    # pylint: disable-next=:binary-op-exception
    except ImportError or ModuleNotFoundError:
        pass
else:
    # LOCALFOLDER LIBRARY
    from .prod import *

print(DATABASES)
raise "stop here to check database"
