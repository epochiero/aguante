import os
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')

# Application definition
INSTALLED_APPS = (
    'frontend',
    'futbol',

    # Third-party
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS':
        {
            'debug': True,
            'context_processors': (
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth'
            )
        }
    },
]

ROOT_URLCONF = 'aguante.urls'

WSGI_APPLICATION = 'aguante.wsgi.application'


# Internationalization
LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Media files (user-uploaded)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'


# Third-party apps configuration
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s: %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': 'aguante.log'
        },
    },
    'loggers': {
        'frontend': {
            'handlers': ['console', ],
            'level': 'DEBUG'
        },
        'futbol': {
            'handlers': ['console', ],
            'level': 'DEBUG'
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
