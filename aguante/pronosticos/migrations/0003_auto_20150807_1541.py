# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pronosticos', '0002_fecha_activa'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='equipos_cargados',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='torneo',
            name='equipos',
            field=models.ManyToManyField(to='pronosticos.Equipo', blank=True, related_name='torneos'),
        ),
    ]
