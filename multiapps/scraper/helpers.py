"""
This module helps other module to extract and prepar data for client
"""

# STDLIB LIBRARY
import logging
from datetime import timedelta, timezone

# THIRDPARTY LIBRARY
import pytube

# FIRSTPARTY LIBRARY
from backend.settings import env
from scraper.models import ChannelMongo, CommentMongo, Video, VideoMongo
from scraper.utils import calc_time_ago, format_duration, numberize



logger = logging.getLogger(__name__)


def prepare_videos_context(c_obj=None):
  """
  Prepare videos context like id, title, thumbnail, duration, views and publish date
  """

  if not c_obj:
    return {}

  contexts = {
    'videos': [],
    'channel': {
      'url': c_obj.channel_id,
      'title': c_obj.title,
    },
  }

  try:
    logger.debug(f'fetching channel\'s thumbnails_url from mongodb for c_obj={c_obj}')
    contexts['channel']['profile_url'] = ChannelMongo.objects.get(m_channel=c_obj.id).thumbnails_url
    logger.info('fetched channel\'s thumbnails_url from mongodb')
  except Exception as e:
    contexts['channel']['profile_url'] = ''
    logger.exception('failed to fetch channel\'s thumbnails_url from mongodb')


  for v_obj in c_obj.videos.iterator():
    try:
      logger.debug(f'extracting video content from video obj={v_obj}')
      contexts['videos'].append({
        'thumbnail_url': VideoMongo.objects.get(m_video=v_obj.id).thumbnails_url,
        'video_id': v_obj.video_id,
        'title': v_obj.title,
        'duration': format_duration(v_obj.duration),
        'view_count': numberize(v_obj.view_count),
        'publish_at': calc_time_ago(v_obj.publish_at),
      })
    except Exception as e:
      logger.exception('failed to extract video content from video obj={v_obj}')

  logger.info(f'extracted content details for {len(contexts["videos"])} videos ')

  return contexts


def prepare_video_metadata(v_obj=None):
  """
  Prepare video metadata just like prepare_videos_context with additional information such as description and comments
  """

  if not v_obj:
    return {}

  contexts = prepare_videos_context(v_obj.channel)
  contexts['channel']['subscriber'] = numberize(v_obj.channel.subscriber)

  try:
    logger.debug(f'extracting video content from video obj={v_obj}')
    contexts['video_metadata'] = {
      'id': v_obj.video_id,
      'title': v_obj.title,
      'view_count': '{:,}'.format(v_obj.view_count),
      'like_count': numberize(v_obj.like_count)[:-2],
      'publish_at': v_obj.publish_at.strftime('%b %d, %Y'),
      'comment_count': v_obj.comment_count,
    }
  except Exception as e:
    contexts['video_metadata'] = {}
    logger.exception('failed to extract video content from video obj={v_obj}')

  logger.info('extracted video content from video obj')

  try:
    logger.debug(f'fetching video\'s description from mongodb for v_obj={v_obj}')
    contexts['video_metadata']['description'] = VideoMongo.objects.get(m_video=v_obj.id).mv_description
    logger.info('fetched video\'s description from mongodb')
  except:
    contexts['video_metadata']['description'] = ''
    logger.exception('failed to fetch video\'s description from mongodb for v_obj={v_obj}')

  try:
    logger.debug(f'fetching video\'s comments from mongodb for v_obj={v_obj}')
    v_comments = CommentMongo.objects.filter(video=v_obj.id)
    logger.info('fetched video\'s comments from mongodb')
  except:
    logger.exception('failed to fetch video\'s comments from mongodb for v_obj={v_obj}')


  contexts['video_metadata']['comments'] = []
  for comment in v_comments.iterator():
    try:
      logger.debug(f'extracting comment for video obj={v_obj}')
      contexts['video_metadata']['comments'].append({
        'commenter': comment.commenter,
        'channel_id': comment.commenter_channel_id,
        'profile_url': comment.thumbnails_url,
        'comment_text': comment.comment,
        'comment_at': calc_time_ago(comment.comment_at),
      })
    except Exception as e:
      logger.exception(f'failed to extract comment for video obj={v_obj}')

  logger.info(f'extracted video\'s comments')

  return contexts


def get_channels_videos(channel=None):
  """
  Get channel's video and its information such as id, title, duration, publish date, views, comments
  """
  if not channel:
    return ([], [])

  c = pytube.Channel(url=f'https://www.youtube.com/channel/{channel.channel_id}')

  records = []
  documents = []
  v_count = 1

  for video in c.videos_generator():
    try:
      logger.debug(f'fetching details for video={video}')
      v = Video(**{
        'video_id': video.video_id,
        'title': video.title,
        'duration': timedelta(seconds=video.length),
        'publish_at': video.publish_date.replace(tzinfo=timezone.utc),
        'view_count': video.views,
        'like_count': int(
          video.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
            'videoPrimaryInfoRenderer'
          ]['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText'][
            'simpleText'
          ]
        ),
        'comment_count': int(
          video.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][2][
            'itemSectionRenderer'
          ]['contents'][0]['commentsEntryPointHeaderRenderer']['commentCount']['simpleText']
        ),
        'channel': channel,
      })

      vm = VideoMongo(**{'m_video': v, 'mv_description': video.description, 'thumbnails_url': video.thumbnail_url})

    except Exception as e:
      logger.exception(f'failed to fetch details for video={video}')

    else:
      v_count += 1
      records.append(v)
      documents.append(vm)

      if v_count > env.int('MAX_VIDEOS_FROM_CHANNEL'):
        break

  logger.info(f'fetched details of videos')

  return (records, documents)


def get_video_streams(v_id=None):
  """
  Get video streams to download video
  """

  if not v_id:
    return None

  try:
    logger.debug(f'getting pyt_obj for video id={v_id}')
    pyt_obj = pytube.YouTube(url=f'https://www.youtube.com/watch?v={v_id}')
    logger.info(f'got pyt_obj for video id={v_id}')
  except Exception as e:
    logger.exception(f'failed to fetch pyt_obj={pyt_obj}')

  video_streams = []
  for stream in pyt_obj.streams.filter(file_extension='mp4', type="video").order_by('resolution').desc():
    try:
      logger.debug(f'extracting stream for {stream}')
      video_streams.append({
        'size': f'{stream.filesize/10**6:.2f}MB',
        'progressive': stream.is_progressive,
        'resolution': stream.resolution,
        'fps': f'{stream.fps}FPS',
        'url': stream.url,
      })
    except:
      logger.exception(f'failed to extract stream for {stream}')

  logger.info('extracted all strams for video')

  return video_streams


def get_search_videos(query='', n_videos=0):
  """
  Get videos based on search query
  """

  contexts = {
    'videos': [],
  }
  v_count = 0

  search = pytube.Search(query)
  # search.get_next_results()
  for v_obj in search.results:
    try:
      logger.debug(f'extracting video content for search_query={query}, video obj={v_obj}')
      contexts['videos'].append({
        'thumbnail_url': v_obj.thumbnail_url,
        'video_id': v_obj.video_id,
        'title': v_obj.title,
        'duration': format_duration(v_obj.length),
        'view_count': numberize(v_obj.views),
        'publish_at': calc_time_ago(v_obj.publish_date),
        'channel': {
          'url': v_obj.channel_id,
          'title': v_obj.author,
          'profile_url': v_obj.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['thumbnail']['thumbnails'][-1]['url']
        },
      })

    except:
      logger.debug(f'{v_obj.vid_info.keys()}')
      logger.exception(f'failed to extract video content for search_query={query}, video obj={v_obj}')

    else:
      v_count += 1
      if v_count > n_videos:
        break

  logger.info('extracted videos content details')
    
  return contexts
