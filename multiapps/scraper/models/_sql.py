"""
Models for Storing data on sql
"""

# THIRDPARTY LIBRARY
from djongo import models

# DJANGO LIBRARY
from django.core.exceptions import ValidationError



class Video(models.Model):
  """
  Store video data on sql
  """

  video_id = models.CharField(unique=True, max_length=32)
  title = models.CharField(unique=True, max_length=128)
  duration = models.DurationField()
  publish_at = models.DateTimeField()
  view_count = models.PositiveIntegerField()
  like_count = models.PositiveIntegerField()
  comment_count = models.PositiveIntegerField()
  channel = models.ForeignKey(to='scraper.Channel', related_name='videos', on_delete=models.CASCADE)

  class Meta:
    verbose_name = 'Video'
    ordering = ('-publish_at', '-view_count', '-like_count', '-comment_count')

  def __repr__(self):
    return f'<VideoModel: video_id={self.video_id}, title={self.title}, channel={self.channel}>'


class Channel(models.Model):
  """
  Store Comment data on sql
  """

  channel_id = models.CharField(unique=True, blank=True, max_length=32)
  custom_url = models.CharField(unique=True, blank=True, max_length=32)
  title = models.CharField(blank=True, max_length=128)
  subscriber = models.PositiveIntegerField(blank=True, default=0)
  last_updated = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Channel'
    unique_together = ('channel_id', 'custom_url')

  def __repr__(self):
    return f'<ChannelModel: channel_id={self.channel_id}, title={self.title}>'

  def clean(self):
    if not self.channel_id and not self.custom_url:
      raise ValidationError(
        {
          'channel_id': 'channel_id and custom_url not allow blank togather',
          'custom_url': 'Even one of channel_id or custom_url should have a value',
        }
      )
