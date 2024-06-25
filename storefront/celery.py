from celery import Celery
import os

print("Active Celery Module")

os.environ.setdefault('DJANGO_SETTING_MODULE', 'storefront.setting')
# Set enviroment Variable to default #
app= Celery(main='storefront', broker='redis://localhost:6379/1') # Module Name
app.autodiscover_tasks()