from django.apps import AppConfig
# import redis
#
#
# red = redis.Redis(
#     host='redis-16312.c302.asia-northeast1-1.gce.cloud.redislabs.com',
#     port=16312,
#     password='zJ9vQQN9wDzolR8MJbWBnjL6fwFD6Kma'
# )


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from . import signals

