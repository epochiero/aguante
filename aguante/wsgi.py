import os
from dj_static import Cling
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aguante.settings")

from django.core.wsgi import get_wsgi_application
application = Cling(get_wsgi_application())
