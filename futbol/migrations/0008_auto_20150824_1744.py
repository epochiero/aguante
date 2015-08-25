# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0007_auto_20150824_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='youtube_url',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
