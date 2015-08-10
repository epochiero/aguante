import shutil
import tempfile

from django.conf import settings
from django.test import TestCase
from futbol.models import *


class TestEquipos(TestCase):

    def setUp(self):
        # Crear torneos primero
        self.torneo_20 = Torneo.objects.create(
            nombre="Torneo Transicion 2014", universofutbol_id="896")
        self.torneo_30 = Torneo.objects.create(
            nombre="Torneo 2015", universofutbol_id="945")

        # Usar un MEDIA_ROOT temporal para probar
        # la carga de escudos, entre otros
        settings._original_media_root = settings.MEDIA_ROOT
        self._temp_media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self._temp_media_root

    def test_cargar_equipos(self):
        self.torneo_20.cargar_equipos()
        self.assertTrue(self.torneo_20.equipos_cargados)
        self.assertEqual(self.torneo_20.equipos.count(), 20)

        self.torneo_30.cargar_equipos()
        self.assertTrue(self.torneo_30.equipos_cargados)
        self.assertEqual(self.torneo_30.equipos.count(), 30)

        # cargar_equipos() es idempotente
        self.torneo_20.cargar_equipos()
        self.assertTrue(self.torneo_20.equipos_cargados)
        self.assertEqual(self.torneo_20.equipos.count(), 20)

        self.torneo_30.cargar_equipos()
        self.assertTrue(self.torneo_30.equipos_cargados)
        self.assertEqual(self.torneo_30.equipos.count(), 30)

    def test_cargar_fechas(self):
        self.torneo_20.cargar_fechas()
        self.assertEqual(self.torneo_20.fechas.count(), 19)

        self.torneo_30.cargar_fechas()
        self.assertEqual(self.torneo_30.fechas.count(), 30)

        # cargar_fechas() es idempotente
        self.torneo_20.cargar_fechas()
        self.assertEqual(self.torneo_20.fechas.count(), 19)

        self.torneo_30.cargar_fechas()
        self.assertEqual(self.torneo_30.fechas.count(), 30)

    def test_torneo_activo(self):
        torneo_activo = Torneo.get_activo()
        # Por defecto, un torneo no está activo
        self.assertIsNone(torneo_activo)

        self.torneo_20.activo = True
        self.torneo_20.save()
        self.assertEqual(Torneo.get_activo(), self.torneo_20)
        self.torneo_30.activo = True
        self.torneo_30.save()
        self.assertEqual(Torneo.get_activo(), self.torneo_30)
        self.assertNotEqual(Torneo.get_activo(), self.torneo_20)

    def test_fecha_activa(self):
        self.torneo_20.cargar_fechas()
        fecha_activa = self.torneo_20.get_fecha_activa()
        # Por defecto, una fecha no está activa
        self.assertIsNone(fecha_activa)

        fecha_1 = self.torneo_20.fechas.get(numero=1)
        fecha_1.activa = True
        fecha_1.save()
        self.assertEqual(self.torneo_20.get_fecha_activa(), fecha_1)
        fecha_2 = self.torneo_20.fechas.get(numero=2)
        fecha_2.activa = True
        fecha_2.save()
        self.assertEqual(self.torneo_20.get_fecha_activa(), fecha_2)
        self.assertNotEqual(self.torneo_20.get_fecha_activa(), fecha_1)

    def tearDown(self):
        # Borrar el MEDIA_ROOT temporal
        shutil.rmtree(self._temp_media_root, ignore_errors=True)
        settings.MEDIA_ROOT = settings._original_media_root
        del settings._original_media_root
