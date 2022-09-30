"""
Controlling which model should be contained in which database
"""

# STDLIB LIBRARY
import logging

# DJANGO LIBRARY
from django.db.utils import ConnectionRouter



logger = logging.getLogger(__name__)


class ScraperRouter(ConnectionRouter):
  """
  A router to control database operations on models in the scraper app
        db_models = {
          'db_name': {
            'app_name': [
              'models_name'
            ]
          }
        }
  """

  db_models = {
    
    'default': {
      'scraper': [
        'Channel',
        'Setting',
        'Video',
        # 'ChannelMongo',
        # 'VideoMongo',
        # 'CommentMongo',
      ],
      'auth': [
        'group',
        'group_permissions',
        'permission',
        'user',
        'user_groups',
        'user_user_permissions',
      ],
      'django': [
        'admin_log',
        'content_type',
        'migrations',
        'session',
      ],
      'sqlite': [
        'sequence',
      ],
    },

    'mongodb': {
      'scraper': [
        'ChannelMongo',
        'VideoMongo',
        'CommentMongo',
      ],
    },

  }


  @classmethod
  def get_db_name_for_model(cls, model_name):
    """
    Finding database name for model
    """
    
    _app,_model = model_name.lower().split('_', 1)
    for db,apps in cls.db_models.items():
      if _app in apps.keys():
        if _model in apps[_app] or _model in map(str.lower, apps[_app]):
          logger.info(f'"{model_name}" model found in "{db}" database ')
          return db
        else:
          logger.info(f'for db="{db}" and app="{_app}", model="{_model}" not found in models={apps[_app]}')
    else:
      logger.critical(f'The name of model "{_model}" must te nested under db_model={dict({_app:["expected here"]})}')


  def db_for_read(self, model, **hints):
    """
    Attempts to read data for model from database.
    """
    
    model_name = model._meta.db_table
    db = self.get_db_name_for_model(model_name)
    logger.debug(f'accessing "{model_name}" model from "{db}" database to read data')
    return db


  def db_for_write(self, model, **hints):
    """
    Attempts to write data for model in database.
    """
    
    model_name = model._meta.db_table
    db = self.get_db_name_for_model(model_name)
    logger.debug(f'accessing "{model_name}" model from "{db}" database to write data')
    return db

  def allow_relation(self, obj1, obj2, **hints):
    """
    Attempts to make relation between models which comes from different database.
    """
    
    logger.debug(f'allow model relation between {obj1} and {obj2}')
    return True

  def allow_migrate(self, db, app_label, model_name=None, **hints):
    """
    Attempts to migrate models in database.
    """

    logger.debug(f'allow_migrate for db={db}, app_label={app_label}, model_name={model_name}, hints={hints}')
    
    if app_label in self.db_models.keys():
      models = self.db_models[db][app_label]
      if model_name in models or model_name in map(str.lower, models):
        logger.debug(f'return True for db={db}, app_label={app_label}, model_name={model_name}, hints={hints}')
        return True
      else:
        logger.debug(f'return False for db={db}, app_label={app_label}, model_name={model_name}, hints={hints}')
        return False

    logger.debug(f'return None for db={db}, app_label={app_label}, model_name={model_name}, hints={hints}')
    return None
