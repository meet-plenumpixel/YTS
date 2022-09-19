"""
Endpoint for accessing Youtube API
"""

# STDLIB LIBRARY
import logging
import os

# THIRDPARTY LIBRARY
from googleapiclient.discovery import build

# FIRSTPARTY LIBRARY
from backend.settings import env



logger = logging.getLogger(__name__)


class Youtube:
  singleton_yt = None

  @staticmethod
  def __youtube():
    """
    Singleton Youtube object to build single connection for all class instance
    """

    try:
      logger.debug(f'getting Youtube singleton object when Youtube.singleton_yt={Youtube.singleton_yt}')

      if Youtube.singleton_yt is None:
        Youtube.singleton_yt = build('youtube', 'v3', developerKey=env.str("YT_API_KEY"))
        logger.info('return fresh created Youtube singleton obj')

      else:
        logger.info('return Youtube singleton obj')

    except Exception as e:
      logger.exception(f'failed to access Youtube singleton obj error="{e}"')
      
    return Youtube.singleton_yt


  @classmethod
  def __call_api(cls, request_for=None, **kwargs):
    """
    Execute request of Youtube singleton object
    """

    if not request_for:
      return
    
    try:
      logger.debug(f'getting Youtube singleton object for request_for={request_for}')
      youtube = getattr(cls.__youtube(), request_for)

      logger.debug(f'fetching data from Youtube API for kwargs={kwargs}')
      request = youtube().list(**kwargs)
      
      logger.debug(f'executing Youtube API for request={request}')
      response = request.execute()

      logger.info('fetched youtube API successfully')
    
    except:
      logger.exception('failed to fetch data from Youtube API')
      return {}

    else:
      return response['items']


  def get_channel_detail(self, channels_ids=None, custom_url=None):
    """ Quota Cost: 1
    Fetch channel details for given channel id
    """
    return self.__call_api('channels', 
      part='id,snippet,statistics', 
      id=','.join(channels_ids)
    )


  def get_videos_id_from_channel(self, c_id):
    """ Quota Cost: 100
    Fetch videos id from given channel
    """
    return self.__call_api('search', 
      part='id', 
      channelId=c_id, 
      order='date', 
      type='video'
    )


  def get_videos_details_from_videos_id(self, v_ids):
    """ Quota Cost: 1
    Fetch videos details for given videos_id
    """
    return self.__call_api('channels', 
      part='snippet,contentDetails,statistics', 
      id=','.join(v_ids)
    )


  def get_video_comments_from_video_id(self, v_id):
    """ Quota Cost: 1
    Fetch video comments for given video_id
    """
    return self.__call_api('commentThreads', 
      part='snippet,id', 
      order='time', 
      videoId=v_id
    )
