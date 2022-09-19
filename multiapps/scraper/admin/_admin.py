"""
ModelAdmin for Admin interface
"""

# DJANGO LIBRARY
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# FIRSTPARTY LIBRARY
from scraper.models import Channel, CommentMongo, Video

# LOCALFOLDER LIBRARY
from ._actions import create_channels_videos, get_video_comments
from ._inlines import (
    ChanneMongolInlineAdmin,
    CommentMongoInlineAdmin,
    VideoInlineAdmin,
    VideoMongoInlineAdmin,
)



@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
  """
  Admin interface for Channel model of sql
  """

  list_display = ('title', 'channel_id', 'custom_url', 'subscriber', 'last_updated')
  list_display_links = ('channel_id', 'custom_url', 'title')
  search_fields = ('title', 'channel_id')
  readonly_fields = ('last_updated',)

  inlines = [ChanneMongolInlineAdmin, VideoInlineAdmin]
  actions = [create_channels_videos]

  fieldsets = (
    (None, {'fields': (('channel_id', 'custom_url'), 'title')}),
    (
      'Statistics',
      {
        # 'classes': ('collapse',),
        'fields': ('subscriber', 'last_updated'),
      },
    ),
  )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
  """
  Admin interface for Video model of sql
  """
  
  list_display = (
    'title',
    'video_id',
    'duration',
    'publish_at',
    'view_count',
    'like_count',
    'comment_count',
    'get_channel_name_from_video',
  )
  readonly_fields = ('video_id', 'duration', 'publish_at', 'view_count', 'like_count', 'comment_count')
  search_fields = ('title', 'video_id')

  inlines = [VideoMongoInlineAdmin, CommentMongoInlineAdmin]
  actions = [get_video_comments]

  fieldsets = (
    (None, {'fields': ('video_id', 'title')}),
    (
      'Statistics',
      {
        # 'classes': ('collapse',),
        'fields': (('duration', 'publish_at'), ('view_count', 'like_count', 'comment_count')),
      },
    ),
  )

  @admin.display(description='Channel title')
  def get_channel_name_from_video(self, obj):
    return format_html(
      "{}",
      mark_safe(f'<a href="{reverse("admin:scraper_channel_change", args=(obj.channel.id,))}">{obj.channel.title}</a>'),
    )


@admin.register(CommentMongo)
class CommentMongoAdmin(admin.ModelAdmin):
  """
  Admin interface for comment model of mongodb
  """
  list_display = ('commenter', 'commenter_channel_id')

  # @admin.display(description='Video')
  # def comment_on_video(self, obj):
  #   return format_html("{}",
  #     mark_safe(f'<a href="{reverse("admin:scraper_videos_change", args=(obj.video.id,))}">Video</a>')
  #   )


# @admin.register(ChannelMongo)
# class ChannelMongoAdmin(admin.ModelAdmin):
#   """
#   Admin interface for Channel model of mongodb
#   """
#   list_display = ('thumbnails_url', 'description', 'get_channel_id')
#   list_display_links = ('thumbnails_url', )

#   @admin.display(description='channel_url')
#   def get_channel_url(self, obj):
#     return format_html("{}",
#       mark_safe(f'<a href="{reverse("admin:scraper_channel_change", args=(obj.m_channel_id,))}">channel</a>')
#     )


# @admin.register(VideoMongo)
# class VideoMongoAdmin(admin.ModelAdmin):
#   """
#   Admin interface for Video model of mongodb
#   """
#   list_display = ('m_video', 'mv_description', 'thumbnails_url')
