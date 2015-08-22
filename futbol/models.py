#-*- coding: utf-8 -*-
import logging
import os

from common.models import EstadoPartido
from crawlers.crawlers import UniversoFutbolCrawler
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from io import BytesIO
from urllib.parse import urlparse
from urllib.request import urlopen


logger = logging.getLogger(__name__)


class Equipo(models.Model):

    EQUIPOS_ESCUDOS_PATH = 'equipos'

    """ Modelo para los equipos. """
    nombre = models.CharField(max_length=50)
    escudo = models.ImageField(
        upload_to=EQUIPOS_ESCUDOS_PATH, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Partido(models.Model):

    """ Modelo para los partidos.
    - goles_local y goles_visitante reflejan el resultado real del partido,
      no un pronóstico.
    - fecha se refiere a la fecha del torneo (1º, 2º, etc.)
    - timestamp es la fecha y hora del partido. """
    class Meta:
        unique_together = ('equipo_local', 'equipo_visitante', 'fecha')

    ESTADO_CHOICES = ((EstadoPartido.NO_EMPEZADO, 'No empezado'),
                      (EstadoPartido.EN_JUEGO, 'En juego'),
                      (EstadoPartido.TERMINADO, 'Terminado'),
                      )

    equipo_local = models.ForeignKey('Equipo', related_name='partidos_local')
    goles_local = models.IntegerField(blank=True, null=True)
    equipo_visitante = models.ForeignKey(
        'Equipo', related_name='partidos_visitante')
    goles_visitante = models.IntegerField(blank=True, null=True)
    fecha = models.ForeignKey('Fecha', related_name='partidos_fecha')
    timestamp = models.DateTimeField(blank=True, null=True, auto_now=True)
    estado = models.IntegerField(
        choices=ESTADO_CHOICES, default=EstadoPartido.NO_EMPEZADO)

    def __str__(self):
        return "{local} vs. {visitante}, {torneo}".format(local=self.equipo_local.nombre,
                                                          visitante=self.equipo_visitante.nombre,
                                                          torneo=self.fecha.torneo.nombre)

    @property
    def texto_estado(self):
        if self.estado == EstadoPartido.NO_EMPEZADO:
            return "No empezado"
        elif self.estado == EstadoPartido.EN_JUEGO:
            return "En juego"
        return "Terminado"


class Fecha(models.Model):

    class Meta:
        unique_together = ('numero', 'torneo')

    """ Modelo para una fecha de un torneo. """
    numero = models.PositiveIntegerField()
    torneo = models.ForeignKey('Torneo', related_name='fechas')
    activa = models.BooleanField(default=False)

    def __str__(self):
        return "Fecha {nro} {torneo}".format(nro=self.numero, torneo=self.torneo.nombre)

    def save(self, *args, **kwargs):
        if self.activa:
            try:
                # Marcar como inactiva la fecha anterior (si es que lo está)
                fecha_activa = Fecha.objects.get(activa=True)
                fecha_activa.activa = False
                fecha_activa.save()
            except Fecha.DoesNotExist:
                pass
        return super().save(*args, **kwargs)

    def _get_data_partidos(self):
        # TODO: no instanciar en cada llamada
        crawler = UniversoFutbolCrawler(self.torneo.universofutbol_id)
        return crawler.get_fecha(self.numero)

    def actualizar_partidos(self):
        data_partidos = self._get_data_partidos()

        # Si todos los partidos están terminados, marcar
        # la fecha siguiente como activa
        if set(data_partido['estado'] for data_partido in data_partidos) ==\
                set([EstadoPartido.TERMINADO]) and self.activa:
            try:
                proxima_fecha = self.torneo.fechas.get(
                    numero=self.numero + 1)
                proxima_fecha.activa = True
                proxima_fecha.save()
                logger.info(
                    "La nueva fecha activa es: {}".format(proxima_fecha))
            except Fecha.DoesNotExist:
                # Es la última fecha
                self.activa = False
                self.save()
        else:
            for data_partido in data_partidos:
                logger.info("Actualizando partido: {} - {}".format(
                    data_partido['equipo_local'], data_partido['equipo_visitante']))
                partido, _ = self.partidos_fecha.get_or_create(
                    equipo_local=Equipo.objects.get(
                        nombre=data_partido['equipo_local']),
                    equipo_visitante=Equipo.objects.get(
                        nombre=data_partido['equipo_visitante']))
                partido.goles_local = data_partido['goles_local']
                partido.goles_visitante = data_partido['goles_visitante']
                partido.estado = data_partido['estado']
                partido.save()

    @property
    def partidos(self):
        if not self.partidos_fecha.count():
            self.actualizar_partidos()
        return self.partidos_fecha.order_by('-estado')


class Torneo(models.Model):

    """ Modelo para un torneo. """
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=False)
    universofutbol_id = models.PositiveIntegerField(unique=True)
    equipos = models.ManyToManyField(
        'Equipo', related_name='torneos', blank=True)
    equipos_cargados = models.BooleanField(default=False)
    cantidad_fechas = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.activo:
            try:
                # Marcar como inactivo el torneo anterior (si es que lo
                # está)
                torneo_activo = Torneo.objects.get(activo=True)
                torneo_activo.activo = False
                torneo_activo.save()
            except Torneo.DoesNotExist:
                pass
        return super().save(*args, **kwargs)

    def cargar_equipos(self):
        """ Usa el crawler para buscar nombres y escudos
        de los equipos del torneo. """
        if self.equipos_cargados:
            logger.info("Los equipos ya han sido cargados para este torneo.")
            return
        crawler = UniversoFutbolCrawler(self.universofutbol_id)
        equipos = crawler.get_equipos()

        for equipo in equipos:
            self._cargar_equipo(equipo)
        self.equipos_cargados = True
        self.save()

    def cargar_fechas(self):
        if not self.cantidad_fechas:
            crawler = UniversoFutbolCrawler(self.universofutbol_id)
            self.cantidad_fechas = crawler.get_cantidad_fechas()
            self.save()

        for i in range(1, self.cantidad_fechas + 1):
            if not Fecha.objects.filter(numero=i, torneo=self).exists():
                fecha = Fecha(numero=i, torneo=self)
                fecha.save()

    def get_fecha_activa(self):
        """ Devuelve la fecha activa del torneo. """
        try:
            return self.fechas.get(activa=True)
        except Fecha.DoesNotExist:
            return None

    @classmethod
    def get_activo(cls):
        """ Devuelve el torneo activo. """
        try:
            return cls.objects.get(activo=True)
        except cls.DoesNotExist:
            return None

    def _cargar_equipo(self, equipo):
        logger.info("Cargando equipo para {torneo}: {equipo}".format(
            torneo=self.nombre, equipo=equipo['nombre']))

        nuevo_equipo, created = Equipo.objects.get_or_create(
            nombre=equipo['nombre'])
        if created:
            # Obtener imagen del escudo
            escudo_url = equipo['escudo_url']
            imagen_path = urlparse(escudo_url).path.split('/')[-1]
            local_imagen_path = os.path.join(
                settings.MEDIA_ROOT, Equipo.EQUIPOS_ESCUDOS_PATH, imagen_path)
            if not os.path.exists(local_imagen_path):
                imagen = urlopen(escudo_url)
                imagen_io = BytesIO(imagen.read())
                nuevo_equipo.escudo.save(imagen_path, File(imagen_io))
            else:
                nuevo_equipo.escudo = os.path.join(
                    Equipo.EQUIPOS_ESCUDOS_PATH, imagen_path)
            nuevo_equipo.save()
        self.equipos.add(nuevo_equipo)
