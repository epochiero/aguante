from django.test import TestCase
from futbol.models import *


class TestEquipos(TestCase):

    def setUp(self):
        # Crear torneos primero
        self.torneo_20 = Torneo.objects.create(
            nombre="Torneo Transicion 2014", universofutbol_id="896")
        self.torneo_30 = Torneo.objects.create(
            nombre="Torneo 2015", universofutbol_id="945")

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
