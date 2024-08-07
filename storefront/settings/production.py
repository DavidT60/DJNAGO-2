import os 
from .common import * 

DEBUG = False 
SECRET_KEY = os.environ['SECRET_KEY']
 # SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS =['server ip address']
