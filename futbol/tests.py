import shutil
import tempfile
from collections import namedtuple

from django.conf import settings
from django.test import TestCase

from futbol.models import *

TorneoTest = namedtuple('TorneoTest', ['torneo', 'num_equipos'])
FechaTest = namedtuple('FechaTest', ['fecha', 'num_equipos'])

class TestEquipos(TestCase):

    @classmethod
    def setUpClass(cls):
        # Usar un MEDIA_ROOT temporal para probar
        # la carga de escudos, entre otros
        settings._original_media_root = settings.MEDIA_ROOT
        cls._temp_media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = cls._temp_media_root

    def setUp(self):
        # Crear torneos primero
        self.torneos = []
        self.torneos.append(TorneoTest(Torneo.objects.create(
            nombre="Torneo 2015", universofutbol_id="945"), 30))
        self.torneos.append(TorneoTest(Torneo.objects.create(
            nombre="Torneo 2016", universofutbol_id="1050"), 30))
        self.torneos.append(TorneoTest(Torneo.objects.create(
            nombre="Torneo 2016/17", universofutbol_id="1093"), 30))
        self.torneos.append(TorneoTest(Torneo.objects.create(
            nombre="Torneo 2017/18", universofutbol_id="1213"), 28))

    def test_cargar_equipos(self):
        # cargar_equipos() es idempotente
        for i in range(2):
            for torneo in self.torneos:
                torneo.torneo.cargar_equipos()
                self.assertTrue(torneo.torneo.equipos_cargados)
                self.assertEqual(torneo.torneo.equipos.count(), torneo.num_equipos)

        for torneo in self.torneos:
            # escudos
            for equipo in torneo.torneo.equipos.all():
                self.assertNotEqual(equipo.escudo, None)

    def test_escudos_en_disco_no_se_borran(self):
        # TODO: validar que cuando se borra el equipo, la imagen queda en disco
        pass

    def test_torneo_activo(self):
        torneo_activo = Torneo.get_activo()
        # Por defecto, un torneo no está activo
        self.assertIsNone(torneo_activo)
        self.torneo_2016.activo = True
        self.torneo_2016.save()
        self.assertEqual(Torneo.get_activo(), self.torneo_2016)
        self.torneo_2016_17.activo = True
        self.torneo_2016_17.save()
        self.assertEqual(Torneo.get_activo(), self.torneo_2016_17)
        self.assertNotEqual(Torneo.get_activo(), self.torneo_2016)

    @classmethod
    def tearDownClass(cls):
        # Borrar el MEDIA_ROOT temporal
        shutil.rmtree(cls._temp_media_root, ignore_errors=True)
        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root


class TestFechas(TestCase):

    def setUp(self):
        # Crear torneos primero
        self.torneo_2015 = Torneo.objects.create(
            nombre="Torneo 2015", universofutbol_id="945")
        self.torneo_2016 = Torneo.objects.create(
            nombre="Torneo 2016", universofutbol_id="1050")
        self.torneo_2016_17 = Torneo.objects.create(
            nombre="Torneo 2016/17", universofutbol_id="1093")

        # Crear fechas
        self.torneo_2015.cargar_fechas()
        self.torneo_2016.cargar_fechas()
        self.torneo_2016_17.cargar_fechas()

    def test_cargar_fechas(self):
        # cargar_fechas() es idempotente
        for i in range(2):
            self.assertEqual(
                self.torneo_2015.fechas.count(), self.torneo_2015.cantidad_fechas)
            self.assertEqual(
                self.torneo_2016.fechas.count(), self.torneo_2016.cantidad_fechas)
            self.assertEqual(
                self.torneo_2016_17.fechas.count(), self.torneo_2016_17.cantidad_fechas)

    def test_fecha_activa(self):
        fecha_activa = self.torneo_2016_17.get_fecha_activa()
        # Por defecto, una fecha no está activa
        self.assertIsNone(fecha_activa)

        fecha_1 = self.torneo_2016_17.fechas.get(numero=1)
        fecha_2 = self.torneo_2016_17.fechas.get(numero=2)
        fecha_1.activa = True
        fecha_1.save()
        self.assertEqual(self.torneo_2016_17.get_fecha_activa(), fecha_1)

        fecha_1.terminar_fecha()
        self.assertEqual(self.torneo_2016_17.get_fecha_activa(), fecha_2)
        self.assertNotEqual(self.torneo_2016_17.get_fecha_activa(), fecha_1)

    def test_get_partidos_fecha(self):
        self.torneo_2016_17.cargar_equipos()
        fecha_1 = self.torneo_2016_17.fechas.get(numero=1)
        fecha_1.actualizar_partidos()
        partidos = fecha_1.partidos.all()
        equipos_partidos = []
        equipos_partidos.extend(
            [partido.equipo_local for partido in partidos])
        equipos_partidos.extend(
            [partido.equipo_visitante for partido in partidos])
        for equipo in self.torneo_2016_17.equipos.all():
            self.assertIn(equipo, equipos_partidos)
