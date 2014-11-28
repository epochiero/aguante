#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models

from io import BytesIO
import logging
from urllib.parse import urlparse
from urllib.request import urlopen

from crawlers.crawlers import UniversoFutbolCrawler

__all__ = ('Equipo', 'Partido', 'Fecha', 'Torneo', 'Pronostico',)

logger = logging.getLogger(__name__)


class Equipo(models.Model):

    """ Modelo para los equipos. """
    nombre = models.CharField(max_length=50)
    escudo = models.ImageField(
        upload_to='equipos', blank=True, null=True)

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
    universofutbol_id = models.PositiveIntegerField()
    equipos = models.ManyToManyField(
        'Equipo', related_name='torneos', blank=True, null=True)

    def __str__(self):
        return self.nombre

    def cargar_equipos(self):
        crawler = UniversoFutbolCrawler(self.universofutbol_id)
        equipos = crawler.get_equipos()

        for equipo in equipos:
            self._cargar_equipo(equipo)

    def _cargar_equipo(self, equipo):
        logger.info("Cargando equipo para {torneo}: {equipo}".format(
            torneo=self.nombre, equipo=equipo['nombre']))

        # Obtener imagen del escudo
        escudo_url = equipo['escudo_url']
        imagen = urlopen(escudo_url)
        imagen_io = BytesIO(imagen.read())
        imagen_path = urlparse(escudo_url).path.split('/')[-1]

        nuevo_equipo = Equipo(nombre=equipo['nombre'])
        nuevo_equipo.escudo.save(imagen_path, File(imagen_io))
        nuevo_equipo.save()
        self.equipos.add(nuevo_equipo)
        self.save()


class Pronostico(models.Model):

    """ Modelo para un pronóstico de un partido. """
    user = models.ForeignKey(User, related_name='pronosticos')
    partido = models.ForeignKey('Partido')
    goles_local = models.IntegerField(blank=True, null=True)
    goles_visitante = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'partido')
