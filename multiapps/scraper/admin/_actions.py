"""
Admin actions to perform database queries in bulk at once
"""

# STDLIB LIBRARY
import json
import logging
import os

# DJANGO LIBRARY
from django.contrib import admin, messages

# FIRSTPARTY LIBRARY
from scraper import helpers
from scraper.models import CommentMongo, Video, VideoMongo
from scraper.youtubeapis import Youtube



logger = logging.getLogger(__name__)


@admin.action()
def get_video_comments(modeladmin, request, queryset):
  """
  Get comments of each video selected in queryset
  """

  records = []
  for video in queryset:

    try:
      logger.debug(f'fethcing comments for video={video} by calling Youtube API')
      yt = Youtube()
      items = yt.get_video_comments_from_video_id(video.video_id)
      logger.info('fethced comments for video by calling Youtube API')

    except Exception as e:
      logger.exception(f'failed to get comments for video={video}')

    logger.debug(f'extracting video={video} comments from Youtube API response')
    for item in items:
      try:
        item = item['snippet']['topLevelComment']['snippet']
        cm = CommentMongo(
          **{
            'video': video,
            'commenter': item['authorDisplayName'],
            'commenter_channel_id': item['authorChannelId']['value'],
            'thumbnails_url': item['authorProfileImageUrl'],
            'comment': item['textOriginal'],
            'comment_at': item['updatedAt'],
          }
        )
      except Exception as e:
        logger.exception(f'failed to extract comment for video={video}')
      else:
        records.append(cm)
    logger.info(f'{len(records)} comments extracted')

  try:
    logger.debug(f'creating comment objs on mongo for video={video}')
    n = CommentMongo.objects.bulk_create(records, batch_size=10)
    messages.add_message(request, messages.SUCCESS, f'new {len(n)} comments added')
    logger.info(f'{len(n)} comments created on mongo')
  except Exception as e:
    logger.exception(f'failed to save comments on mongo for video={video}')

  logger.info('all comments created from selected videos queryset ')


@admin.action()
def get_channels_videos(modeladmin, request, queryset):
  """
  Create videos for each channel in channel queryset
  """

  for channel in queryset:
    try:
      logger.debug(f'extracting videos for channel={channel}')
      records, documents = helpers.get_channels_videos(channel)
      logger.debug(f'extracted videos for channel={channel}')

      logger.debug('creating videos obj on sql')
      n = Video.objects.bulk_create(
        records, batch_size=10
      )  # update_fields=['v_id', 'title', 'duration', 'publish_at', 'view_count', 'like_count', 'comment_count', 'channel'],
      logger.info(f'{n} videos obj created on sql')
      logger.debug('creating videos obj on mongo')
      VideoMongo.objects.bulk_create(documents, batch_size=10)
      logger.info(f'{n} videos obj created on mongo')
      messages.add_message(request, messages.SUCCESS, f'new {len(n)} videos added')

    except Exception as e:
      logger.exception(f'failed to create videos for channel={channel}')

  logger.info('all videos created from selected channels queryset ')


@admin.action()
def force_to_apply_config(modeladmin, request, queryset):
  """
  Force to apply config immediately
  """

  for key,value in queryset.values_list("key", "value"):
    os.environ[key] = value
    logger.debug(f'SET {key}="{value}"')
