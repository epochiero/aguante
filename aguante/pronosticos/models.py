#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

__all__ = ('Equipo', 'Partido', 'Fecha', 'Torneo', 'Pronostico',)


class Equipo(models.Model):

    """ Modelo para los equipos. """
    nombre = models.CharField(max_length=50)
    escudo = models.ImageField(
        upload_to='equipos_media', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Partido(models.Model):

    """ Modelo para los partidos.
    - goles_local y goles_visitante reflejan el resultado real del partido,
      no un pronóstico.
    - fecha se refiere a la fecha del torneo (1º, 2º, etc.)
    - timestamp es la fecha y hora del partido. """
    equipo_local = models.ForeignKey('Equipo', related_name='partidos_local')
    goles_local = models.IntegerField(blank=True, null=True)
    equipo_visitante = models.ForeignKey(
        'Equipo', related_name='partidos_visitante')
    goles_visitante = models.IntegerField(blank=True, null=True)
    fecha = models.ForeignKey('Fecha', related_name='partidos')
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{local} vs. {visitante}, {torneo}".format(local=self.equipo_local.nombre,
                                                          visitante=self.equipo_visitante.nombre,
                                                          torneo=self.fecha.torneo.nombre)


class Fecha(models.Model):

    """ Modelo para una fecha de un torneo. """
    numero = models.PositiveIntegerField()
    torneo = models.ForeignKey('Torneo', related_name='fechas')

    def __str__(self):
        return "Fecha {nro} {torneo}".format(nro=self.numero, torneo=self.torneo.nombre)


class Torneo(models.Model):

    """ Modelo para un torneo. """
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=False)
    equipos = models.ManyToManyField('Equipo', related_name='torneos')

    def __str__(self):
        return self.nombre


class Pronostico(models.Model):

    """ Modelo para un pronóstico de un partido. """
    user = models.ForeignKey(User, related_name='pronosticos')
    partido = models.ForeignKey('Partido')
    goles_local = models.IntegerField(blank=True, null=True)
    goles_visitante = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'partido')
