"""
Inline admin interface for respective models
"""

# DJANGO LIBRARY
from django.contrib import admin

# FIRSTPARTY LIBRARY
from scraper.models import ChannelMongo, CommentMongo, Video, VideoMongo



class ChanneMongolInlineAdmin(admin.StackedInline):
  """
  Inline admin interface for Channel model from mongodb
  """

  model = ChannelMongo
  extra = 1
  can_delete = False
  show_change_link = True


class VideoMongoInlineAdmin(admin.StackedInline):
  """
  Inline admin interface for Video model from mongodb
  """

  model = VideoMongo
  extra = 1
  can_delete = False
  show_change_link = True


class VideoInlineAdmin(admin.TabularInline):
  """
  Inline admin interface for Video model from sql
  """

  model = Video
  extra = 1
  can_delete = False
  show_change_link = True
  readonly_fields = ('video_id', 'duration', 'publish_at', 'view_count', 'like_count', 'comment_count')


class CommentMongoInlineAdmin(admin.StackedInline):
  """
  Inline admin interface for Comment from mongodb
  """

  model = CommentMongo
  extra = 1
  can_delete = False
  show_change_link = True
  fields = (('commenter', 'commenter_channel_id'), 'thumbnails_url', ('comment', 'comment_at'))
  readonly_fields = ('commenter_channel_id', 'comment_at')
