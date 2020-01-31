import shutil
import tempfile

from django.conf import settings
from django.test import TestCase
from futbol.models import *
from crawlers.crawlers import UniversoFutbolCrawler

class BaseTestCase(TestCase):

    def setUp(self):
        # Crear torneos primero
        self.torneo1 = Torneo.objects.create(
            nombre="Torneo 2018/19", universofutbol_id="1279")
        self.torneo2 = Torneo.objects.create(
            nombre="Torneo 2019/20", universofutbol_id="1355")

class TestEquipos(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        # Usar un MEDIA_ROOT temporal para probar
        # la carga de escudos, entre otros
        settings._original_media_root = settings.MEDIA_ROOT
        cls._temp_media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = cls._temp_media_root

    def test_cargar_equipos(self):
        # cargar_equipos() es idempotente
        for i in range(2):
            self.torneo1.cargar_equipos()
            self.assertTrue(self.torneo1.equipos_cargados)
            self.assertEqual(self.torneo1.equipos.count(), 26)

            self.torneo2.cargar_equipos()
            self.assertTrue(self.torneo2.equipos_cargados)
            self.assertEqual(self.torneo2.equipos.count(), 24)

        # escudos
        for equipo in self.torneo1.equipos.all():
            self.assertNotEqual(equipo.escudo, None)
        for equipo in self.torneo2.equipos.all():
            self.assertNotEqual(equipo.escudo, None)


        # borrar equipos pero no los escudos en disco
        Equipo.objects.all().delete()
        self.torneo1.equipos_cargados = False
        self.torneo2.equipos_cargados = False
        self.torneo1.cargar_equipos()
        self.torneo2.cargar_equipos()
        for equipo in self.torneo1.equipos.all():
            self.assertNotEqual(equipo.escudo, None)
        for equipo in self.torneo2.equipos.all():
            self.assertNotEqual(equipo.escudo, None)

    def test_torneo_activo(self):
        torneo_activo = Torneo.get_activo()
        # Por defecto, un torneo no está activo
        self.assertIsNone(torneo_activo)

        self.torneo1.activo = True
        self.torneo1.save()
        self.assertEqual(Torneo.get_activo(), self.torneo1)
        self.torneo2.activo = True
        self.torneo2.save()
        self.assertEqual(Torneo.get_activo(), self.torneo2)
        self.assertNotEqual(Torneo.get_activo(), self.torneo1)

    @classmethod
    def tearDownClass(cls):
        # Borrar el MEDIA_ROOT temporal
        shutil.rmtree(cls._temp_media_root, ignore_errors=True)
        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root


class TestFechas(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Crear fechas
        self.torneo1.cargar_fechas()
        self.torneo2.cargar_fechas()

    def test_cargar_fechas(self):
        # cargar_fechas() es idempotente
        for i in range(2):
            self.assertEqual(
                self.torneo1.fechas.count(), self.torneo1.cantidad_fechas)
            self.assertEqual(
                self.torneo2.fechas.count(), self.torneo2.cantidad_fechas)

    def test_fecha_activa(self):
        fecha_activa = self.torneo2.get_fecha_activa()
        # Por defecto, una fecha no está activa
        self.assertIsNone(fecha_activa)

        fecha_1 = self.torneo2.fechas.get(numero=1)
        fecha_2 = self.torneo2.fechas.get(numero=2)
        fecha_1.activa = True
        fecha_1.save()
        self.assertEqual(self.torneo2.get_fecha_activa(), fecha_1)

        fecha_1.terminar_fecha()
        self.assertEqual(self.torneo2.get_fecha_activa(), fecha_2)
        self.assertNotEqual(self.torneo2.get_fecha_activa(), fecha_1)

    def test_get_partidos_fecha(self):
        self.torneo2.cargar_equipos()
        fecha_1 = self.torneo2.fechas.get(numero=1)
        fecha_1.actualizar_partidos()
        partidos = fecha_1.partidos.all()
        equipos_partidos = []
        equipos_partidos.extend(
            [partido.equipo_local for partido in partidos])
        equipos_partidos.extend(
            [partido.equipo_visitante for partido in partidos])
        for equipo in self.torneo2.equipos.all():
            self.assertIn(equipo, equipos_partidos)
