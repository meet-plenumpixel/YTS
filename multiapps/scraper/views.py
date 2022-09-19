"""
This module handle request within ScraperApp
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView

# FIRSTPARTY LIBRARY
from scraper import helpers
from scraper.models import Channel, Video



logger = logging.getLogger(__name__)


def error_404_view(request, exception):
  """
  Handle 'Page not found error'
  """
  logger.debug('Page not found error')
  return render(request, "error/404.html")


class HomeTemplateView(TemplateView):
  """
  Handle request for index page and it's contents
  """

  template_name = "scraper/index.html"

  def get(self, request, *args, **kwargs):

    try:
      logger.debug('fetching channel\'s id and title')
      self.extra_context = {"channels": Channel.objects.values("channel_id", "title")}  # pylint: disable=no-member
      logger.info('fetched channel\'s id and title')
    except Exception as e:
      logger.exception('failed to fetch data from ChannelModel')

    response = super().get(request, *args, **kwargs)
    return response


class WatchTemplateView(TemplateView):
  """
  Handle request for player page and it's contents
  """

  template_name = "scraper/watch_video.html"

  def get(self, request, *args, **kwargs):
    self.extra_context = {}
    v_id = request.GET.get("v", None)

    try:
      logger.debug(f'fetching video id: id={v_id}')
      v_obj = Video.objects.get(video_id=v_id)  # pylint: disable=no-member
      logger.info(f'fetched video_obj')
    except Exception as e:
      logger.exception('failed to fetch video obj')

    try:
      logger.debug('fetching video metadata for v_obj={v_obj}')
      self.extra_context.update(helpers.prepare_video_metadata(v_obj))
      logger.info('fetched video metadata')
    except Exception as e:
      logger.exception('failed to fetch video metadata')

    try:
      logger.debug(f'fetching video streans for video_id={v_obj.video_id}')
      self.extra_context["video_streams"] = helpers.get_video_streams(v_obj.video_id)
      logger.info('fetched video streans')
    except Exception as e:
      logger.exception('failed to fetch video\'s streams')

    self.extra_context["css_class"] = {"main": "watch"}

    response = super().get(request, *args, **kwargs)
    return response


class VideoTemplateView(TemplateView):
  """
  Handle request for videos page and it's contents
  """

  template_name = "scraper/video_list.html"

  def get(self, request, *args, **kwargs):
    self.extra_context = {}
    c_type = kwargs.get("c_type", None)
    c_url = kwargs.get("c_url", None)

    if c_type == "channel":
      url = {"channel_id": c_url}
    else:
      url = {"custom_url": f"{c_type}/{c_url}"}

    try:
      logger.debug(f'fetching channel obj, otherwise create it for url={url}')
      obj, created = Channel.objects.get_or_create(**url, defaults=url)  # pylint: disable=no-member
      logger.info(f'fetched channel obj')
    except Exception as e:
      logger.exception(f'failed to get_or_create obj for url={url}')

    if created:
      logger.info(f'new request sent to add videos for channel')
      messages.add_message(request, messages.WARNING, "Videos for this channel are not available")
      messages.add_message(request, messages.SUCCESS, "Request has been sent successfully")
      messages.add_message(request, messages.INFO, "Please, Try again in a few minutes")

    else:

      try:
        logger.debug(f'fetching videos context for channel obj={obj}')
        self.extra_context.update(helpers.prepare_videos_context(obj))

        if not self.extra_context['videos']:
          messages.add_message(request, messages.WARNING, "A request for this channel's video has already been sent")
          messages.add_message(request, messages.INFO, "Please, wait for admin approval")
        logger.info(f'fetched videos context')

      except Exception as e:
        logger.exception('failed to prepare videos context')

      try:
        logger.debug('fetching channel\'s id and title')
        self.extra_context["channels"] = Channel.objects.values("channel_id", "title")  # pylint: disable=no-member
        logger.info('channel\'s id and title fetched successfully')
      except Exception as e:
        logger.exception('failed to fetch data from ChannelModel')

    response = super().get(request, *args, **kwargs)
    return response


class SearchRedirectView(TemplateView):
  """
  Handle request for search query
  """

  template_name = "scraper/video_list.html"

  def get(self, request, *args, **kwargs):
    n_videos = int(request.GET.get("n_videos", 10))
    search_query = request.GET.get("search_query", None)

    try:
      logger.debug(f'fetching context for search_query={search_query}')
      self.extra_context = helpers.get_search_videos(search_query, n_videos)
      logger.info(f'fetched context')
    except Exception as e:
      logger.exception(f'failed to fetch context for search_query={search_query}')

    response = super().get(request, *args, **kwargs)
    return response
