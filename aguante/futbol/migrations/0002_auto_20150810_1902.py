# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='torneo',
            name='cantidad_fechas',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
