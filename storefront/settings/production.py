import os 
import dj_database_url
from .common import * 


DEBUG = False 
SECRET_KEY = os.environ['SECRET_KEY']
REDIS_URL = os.environ['REDIS_URL']
 # SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS =['dav-prod-195f10a4c0c4.herokuapp.com/']

DATABASES = {
      'default': dj_database_url.config()
  }

CELERY_BROKER_URL = REDIS_URL
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_BACKEND = os.environ['MAILGUN_SMTP_SERVER'] 
EMAIL_PORT = 2525
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''