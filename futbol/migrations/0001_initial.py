# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('escudo', models.ImageField(null=True, upload_to='equipos', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fecha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('numero', models.PositiveIntegerField()),
                ('activa', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('goles_local', models.IntegerField(null=True, blank=True)),
                ('goles_visitante', models.IntegerField(null=True, blank=True)),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
                ('estado', models.IntegerField(choices=[(0, 'No empezado'), (1, 'En juego'), (2, 'Terminado')], default=0)),
                ('equipo_local', models.ForeignKey(related_name='partidos_local', to='futbol.Equipo', on_delete=models.PROTECT)),
                ('equipo_visitante', models.ForeignKey(related_name='partidos_visitante', to='futbol.Equipo', on_delete=models.PROTECT)),
                ('fecha', models.ForeignKey(related_name='partidos', to='futbol.Fecha', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=False)),
                ('universofutbol_id', models.PositiveIntegerField(unique=True)),
                ('equipos_cargados', models.BooleanField(default=False)),
                ('cantidad_fechas', models.PositiveIntegerField()),
                ('equipos', models.ManyToManyField(related_name='torneos', to='futbol.Equipo', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='fecha',
            name='torneo',
            field=models.ForeignKey(related_name='fechas', to='futbol.Torneo', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='fecha',
            unique_together=set([('numero', 'torneo')]),
        ),
    ]
