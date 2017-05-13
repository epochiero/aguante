from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


app = Celery('aguante', include=['aguante.tasks'])
app.config_from_object('django.conf:settings')
app.conf.update(
    beat_schedule={
        'actualizar_partidos': {
            'task': 'aguante.tasks.actualizar_partidos',
            # Cada minuto entre las 12pm y las 1am
            'schedule': crontab(minute='*', hour='12-23,0'),
        },
    },
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    timezone='America/Argentina/Buenos_Aires',
)

app.autodiscover_tasks(['aguante'])

if __name__ == '__main__':
    app.start()
