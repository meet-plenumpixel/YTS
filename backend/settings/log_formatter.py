"""
Custom 'Formatter for logging module
"""

# STDLIB LIBRARY
import logging
import re



class ColoredFormatter(logging.Formatter):

  FORMATES = {
    logging.DEBUG: "\u001b[36;1m",
    logging.INFO: "\u001b[36m",
    logging.WARNING: "\u001b[33m",
    logging.ERROR: "\u001b[31;1m",
    logging.CRITICAL: "\u001b[31m",
  }

  @classmethod
  def format_attr_by_level(cls, level):
    return lambda attr: cls.FORMATES[level] + attr

  def __init__(self, coler_code=None, *args, **kwargs):
    self.coler_code = coler_code or ''
    return super(ColoredFormatter, self).__init__(*args, **kwargs)

  def format(self, record):
    attr_formatter = self.format_attr_by_level(level=record.levelno)
    list_log_attr = [
      attr_formatter('[{asctime} '),
      "{levelname:^8}] ",
      "( \u001b[0m",
      "\u001b[34;1m{name}\u001b[0m",
      "\u001b[1m:\u001b[0m",
      "\u001b[35;1m{lineno}\u001b[0m",
      "\u001b[1m:\u001b[0m",
      "\u001b[32m{funcName}\u001b[0m",
      attr_formatter(' )\u001b[0m '),
      "{message}",
    ]

    dash_line = '\n' + attr_formatter('-' * 120) if record.exc_info else ''

    formatter = logging.Formatter(''.join(list_log_attr + [dash_line]), style='{')
    log_message = formatter.format(record) + dash_line

    if self.coler_code.upper() == 'ASCII':
      return log_message
    else:
      return re.sub('\\u001b\[\d{0,3};?\d?m', '', log_message)
