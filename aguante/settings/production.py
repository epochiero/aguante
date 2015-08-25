import os
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]

GDATA_ACCESS_KEY = os.environ['GDATA_ACCESS_KEY']

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
