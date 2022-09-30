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
from ._sql import Channel, Video



def validate_upper_case(key_text):
  if not key_text.isupper():
    raise ValidationError(
      _(f'all character of "{key_text}" must be capital')
    )

class Setting(models.Model):
  """
  Store ScraperApp configuration on sql
  """

  key = models.CharField(unique=True, max_length=128, validators=[validate_upper_case])
  value = models.CharField(max_length=128)
  description = models.TextField()

  class Meta:
    verbose_name = 'Settings'
    ordering = ('key',)

  def __repr__(self):
    return f'<ScraperSetting: key={self.key}, value={self.value}>'

  def __str__(self):
      return f'{self.key}'


__all__ = [
  'Setting',
  'Channel',
  'Video',
  'ChannelMongo',
  'VideoMongo',
  'CommentMongo'
]
