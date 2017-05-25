import os
from .base import *

DEBUG = True

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['*']

ADMINS = (
	('Ezequiel Pochiero', 'epochiero@gmail.com'),
)

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, os.environ['DB_PROD']),
    }
}
