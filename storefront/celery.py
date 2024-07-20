from celery import Celery
import os

# DOCUMENTATION WAY: https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#redis
# print("Active Celery Module")

# os.environ.setdefault('DJANGO_SETTING_MODULE', 'storefront.setting')
# # Set enviroment Variable to default #
# app= Celery(main='storefront', broker='redis://localhost:6379/1') # Module Name
# app.autodiscover_tasks()

# Another way 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
app = Celery('storefront')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()