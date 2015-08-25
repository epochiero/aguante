# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0006_auto_20150823_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='nombre_youtube',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='partido',
            name='youtube_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
