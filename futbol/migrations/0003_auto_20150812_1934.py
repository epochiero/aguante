# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0002_auto_20150810_1902'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='partido',
            unique_together=set([('equipo_local', 'equipo_visitante', 'fecha')]),
        ),
    ]
