# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('futbol', '0003_auto_20150812_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='timestamp',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
