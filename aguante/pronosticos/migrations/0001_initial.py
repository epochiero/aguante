# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
                ('escudo', models.ImageField(blank=True, upload_to='equipos', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fecha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('numero', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('goles_local', models.IntegerField(blank=True, null=True)),
                ('goles_visitante', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('estado', models.IntegerField(choices=[(0, 'No empezado'), (1, 'En juego'), (2, 'Terminado')], default=0)),
                ('equipo_local', models.ForeignKey(to='pronosticos.Equipo', related_name='partidos_local')),
                ('equipo_visitante', models.ForeignKey(to='pronosticos.Equipo', related_name='partidos_visitante')),
                ('fecha', models.ForeignKey(to='pronosticos.Fecha', related_name='partidos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pronostico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('goles_local', models.IntegerField(blank=True, null=True)),
                ('goles_visitante', models.IntegerField(blank=True, null=True)),
                ('partido', models.ForeignKey(to='pronosticos.Partido')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='pronosticos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=False)),
                ('universofutbol_id', models.PositiveIntegerField(unique=True)),
                ('equipos', models.ManyToManyField(blank=True, to='pronosticos.Equipo', related_name='torneos', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='pronostico',
            unique_together=set([('user', 'partido')]),
        ),
        migrations.AddField(
            model_name='fecha',
            name='torneo',
            field=models.ForeignKey(to='pronosticos.Torneo', related_name='fechas'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='fecha',
            unique_together=set([('numero', 'torneo')]),
        ),
    ]
