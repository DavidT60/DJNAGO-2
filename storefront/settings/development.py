from .common import *


from .common import * 

EBUG = True 
SECRET_KEY = 'django-insecure-hs6j037urx6iav+7#10%-vu4l4f5@@-1_zo)oft4g7$vf2$jmp'

  #- Database -#
  # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'DJANGO-34',
          'HOST': 'localhost',
          'USER': 'postgres',
          'PASSWORD': '1234'
      }
  }


CELERY_BROKER_URL = 'redis://localhost:6379/1'
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}