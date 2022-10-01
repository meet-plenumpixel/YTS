"""
Models for Storing data on sql and mongodb
"""

# THIRDPARTY LIBRARY
from djongo import models

# DJANGO LIBRARY
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# LOCALFOLDER LIBRARY
from ._mongo import ChannelMongo, CommentMongo, VideoMongo
from ._sql import Channel, Video, Setting



__all__ = [
  'Channel',
  'Video',
  'ChannelMongo',
  'VideoMongo',
  'CommentMongo'
]
