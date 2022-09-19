"""
Models for Storing data on sql
"""

# THIRDPARTY LIBRARY
from djongo import models



class CommentMongo(models.Model):
  """
  Store Comment data on mongodb
  """

  video = models.ForeignKey(to='scraper.Video', related_name='comments', on_delete=models.CASCADE)
  commenter = models.CharField(blank=True, max_length=128)
  commenter_channel_id = models.URLField()
  thumbnails_url = models.URLField()
  comment = models.TextField()
  comment_at = models.DateTimeField()

  class Meta:
    verbose_name = 'Videos Comments'

  def __repr__(self):
    return f'<CommentMongo: video={self.video}, comment_at={self.comment_at}>'


class VideoMongo(models.Model):
  """
  Store Video data on mongodb
  """

  m_video = models.OneToOneField(to='scraper.Video', related_name='from_mongo_video', on_delete=models.PROTECT)
  mv_description = models.TextField()
  thumbnails_url = models.URLField()

  class Meta:
    verbose_name = 'Video OnMongoDB'

  def __repr__(self):
    return f'<VideoMongoModel: m_video={self.m_video}>'


class ChannelMongo(models.Model):
  """
  Store Channel data on mongodb
  """

  # _id = models.ObjectIdField(primary_key=False, auto_created=False)
  m_channel = models.OneToOneField(to='scraper.Channel', related_name='from_mongo_channel', on_delete=models.PROTECT)
  description = models.TextField()
  thumbnails_url = models.URLField()
  # videos = models.EmbeddedField(
  #   model_container=VideoMongo
  # )

  class Meta:
    verbose_name = 'About Channel'

  def __repr__(self):
    return f'<ChannelMongoModel: m_channel={self.m_channel}, thumbnails_url={self.thumbnails_url}>'
