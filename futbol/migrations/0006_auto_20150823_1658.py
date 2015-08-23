# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0005_auto_20150814_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='fecha',
            name='terminada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fecha',
            name='ultima_actualizacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='partido',
            name='timestamp',
            field=models.DateTimeField(null=True, blank=True, default=django.utils.timezone.now),
        ),
    ]
