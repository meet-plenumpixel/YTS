"""
This module processes the signal sent by the model
"""

# STDLIB LIBRARY
import logging

# THIRDPARTY LIBRARY
import pytube

# DJANGO LIBRARY
from django.db.models import signals
from django.dispatch.dispatcher import receiver

# FIRSTPARTY LIBRARY
from scraper import helpers
from scraper.models import (
    Channel,
    ChannelMongo,
    CommentMongo,
    Video,
    VideoMongo,
)



logger = logging.getLogger(__name__)


@receiver(signals.pre_save, sender=Channel)
def update_channel_details_to_sql(sender, instance, *args, **kwargs):
  """
  get title and subscriber along with channel id when new object created
  """

  url = instance.custom_url or 'channel/' + instance.channel_id

  try:
    logger.debug(f'fetching channel details for channel_url={url}')
    c = pytube.Channel(f"https://www.youtube.com/{url}")
    instance.__detail = {
      'description': c.initial_data['metadata']['channelMetadataRenderer']['description'],
      'thumbnails_url': c.initial_data['metadata']['channelMetadataRenderer']['avatar']['thumbnails'][0]['url'],
    }

    instance.channel_id = c.channel_id
    instance.custom_url = c.vanity_url.split('.com/')[1]
    instance.title = c.channel_name

    magnitudeDict = {'': 0, 'K': 3, 'M': 6, 'B': 9, 'T': 12, 'Q': 15}
    subscriber = c.initial_data['header']['c4TabbedHeaderRenderer']['subscriberCountText']['simpleText'].split(' ')[0]

    instance.subscriber = int(float(subscriber[:-1]) * 10 ** magnitudeDict[subscriber[-1:]])
    logger.info('fethed channel details')
  except:
    logger.exception(f'failed to update channel details for channel={instance}')


@receiver(signals.post_save, sender=Channel)
def add_channel_details_to_mongo(sender, instance, created, *args, **kwargs):
  """
  create channel instance on mongodb to store description and thumbnails of channel
  also create videos for the channel and store into both databases (sql and mongo)
  """
  if not  created:
    return

  try:
    logger.debug(f'fetching details for channel obj to update_or_create obj on mongo')
    cm, cm_created = ChannelMongo.objects.update_or_create(m_channel=instance, defaults=instance.__detail)
    logger.info('updated_or_created channel object on mongo')  
  except Exception as e:
    logger.exception(f'failed to update_or_create')

  # if cm_created:
  #   cm.description = detail['description']
  #   cm.thumbnails_url = detail['thumbnails_url']
  #   cm.save()

  # try:
  #   logger.debug('creating video obj in both sql and mongo')
  #   records, documents = helpers.get_channels_videos(instance)
  #   n = Video.objects.bulk_create(
  #     records, batch_size=10
  #   )  # update_fields=['v_id', 'title', 'duration', 'publish_at', 'view_count', 'like_count', 'comment_count', 'channel'],
  #   m =VideoMongo.objects.bulk_create(documents, batch_size=10)
  #   logger.info(f'{n} videos created on sql and {m} videos created on mongo')
  # except:
  #   logger.exception('failed to create video object')


@receiver(signals.pre_delete, sender=Channel)
def delete_document_from_channel_mongo_collections(sender, instance, *args, **kwargs):
  """
  Delete channel obj from mongo when channel obj deleted on sql
  """

  try:
    logger.debug(f'deleting channel obj={instance} from mongo')
    ChannelMongo.objects.filter(m_channel=instance).delete()
    logger.info('channel obj deleted from mongo')
  except:
    logger.exception(f'failed to delete channel obj={instance} from mongo')


@receiver(signals.pre_delete, sender=Video)
def delete_document_from_video_mongo_collections(sender, instance, *args, **kwargs):
  """
  Delete video and associate comments obj from mongo when video obj deleted on sql
  """
  try:
    logger.debug(f'deleting video obj={instance} from mongo')
    VideoMongo.objects.filter(m_video=instance).delete()
    logger.info('video obj deleted from mongo')
    logger.debug(f'deleting comments of video obj={instance} from mongo')
    CommentMongo.objects.filter(video=instance).delete()
    logger.info('comments of video obj deleted from mongo')
  except Exception as e:
    logger.exception(f'failed to delete channel obj={instance} from mongo')
