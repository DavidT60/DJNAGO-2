import os 
import dj_database_url
from .common import * 


DEBUG = False 
SECRET_KEY = os.environ['SECRET_KEY']
REDIS_URL = os.environ['REDISCLOUD_URL']
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT= os.environ['MAILGUN_SMTP_PORT']