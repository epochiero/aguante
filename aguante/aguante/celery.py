from __future__ import absolute_import

from datetime import timedelta
import os

from celery import Celery
from django.conf import settings


app = Celery('aguante', include=['aguante.tasks'])
app.config_from_object('django.conf:settings')
app.conf.update(
    CELERYBEAT_SCHEDULE={
        'actualizar_partidos': {
            'task': 'aguante.tasks.actualizar_partidos',
            'schedule': timedelta(seconds=60),
        },
    })

app.autodiscover_tasks(['aguante'])

if __name__ == '__main__':
    app.start()


