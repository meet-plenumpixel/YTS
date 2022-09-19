"""
This module helps other module to format or manipulate data as per requirement
"""

# STDLIB LIBRARY
# import json
import logging
import re
from datetime import datetime, timedelta, timezone
from math import floor

# THIRDPARTY LIBRARY
import timeago



logger = logging.getLogger(__name__)


# formater = lambda fmt: print(json.dumps(fmt, indent=2))
# parse_datetime = lambda dt: datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S%z')


def numberize(num):
  """
  Convert big number into human readable string
  """

  if not isinstance(num, int):
    num = int(num)

  magnitudeDict = {0: '', 1: 'K', 2: 'M', 3: 'B', 4: 'T', 5: 'Q'}
  num = floor(num)
  magnitude = 0
  while num >= 1000.0:
    magnitude += 1
    num = num / 1000.0
  
  temp = f'{floor(num*100.0)/100.0}{magnitudeDict[magnitude]}'

  logger.debug(f'convert {num} into {temp}')
  return temp


def calc_time_ago(published_time):
  """
  Calculate time duration between given datetime and current datetime to human readable format
  """

  temp = timeago.format(
    published_time if published_time.tzinfo else published_time.replace(tzinfo=timezone.utc),
    datetime.now(tz=timezone.utc),
  )

  logger.debug(f'convert date {published_time} to {temp}')
  return temp


def format_duration(duration):
  """
  Convert timedelta object to human readable format (HH:MM:SS)
  """

  length = duration if isinstance(duration, int) else duration.total_seconds()

  minutes, seconds = map(int, divmod(length, 60))
  hours, minutes = map(int, divmod(minutes, 60))

  total_time = ''
  if hours:
    total_time += f'{hours:02}:'
  if hours or minutes:
    total_time += f'{minutes:02}:'
  total_time += f'{seconds:02}'

  logger.debug(f'convert {duration} to {total_time}')
  return total_time


def iso_to_timedelta(pattern):
  """
  Convert ISO time to timedelta object
  """
  
  ISO_8601_period_rx = re.compile(
    'P'  # designates a period
    # '(?:(?P<years>\d+)Y)?'   # years
    # '(?:(?P<months>\d+)M)?'  # months
    '(?:(?P<weeks>\d+)W)?'     # weeks
    '(?:(?P<days>\d+)D)?'      # days
    '(?:T'                     # time part must begin with a T
    '(?:(?P<hours>\d+)H)?'     # hourss
    '(?:(?P<minutes>\d+)M)?'   # minutes
    '(?:(?P<seconds>\d+)S)?'   # seconds
    ')?'                       # end of time part
  )

  temp = timedelta(**{i: int(j) if j else 0 for i, j in ISO_8601_period_rx.match(pattern).groupdict().items()})

  logger.debug(f'convert {pattern} to {temp}')
  return temp
