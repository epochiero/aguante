import os
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ['DATABASE_HOST'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
    }
}
