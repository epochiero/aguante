# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0004_auto_20150812_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='fecha',
            field=models.ForeignKey(to='futbol.Fecha', related_name='partidos_fecha'),
        ),
    ]
