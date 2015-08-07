#-*- coding: utf-8 -*-
from common.models import EstadoPartido
from pyquery import PyQuery as pq
from urllib.parse import urljoin

__all__ = ['UniversoFutbolCrawler']


class UniversoFutbolCrawler():

    """ Recupera resultados y equipos para un torneo. """

    BASE_URL = "http://www.universofutbol.com/plantillas/archivos/fecha_argentina.php?div=1&camp={camp}&fecha={fecha}"
    EQUIPOS_URL = "http://www.universofutbol.com/plantillas/archivos/noticias.php?div=1&camp={camp}"

    def __init__(self, camp_id):
        self.camp_id = camp_id

    def get_fecha(self, nro_fecha):
        target_url = self.BASE_URL.format(camp=self.camp_id, fecha=nro_fecha)
        html = pq(target_url)

        # td.equipoizquierda matchea el equipo local y el resultado
        # de cada partido de la siguiente forma (empezando con n=0):
        # -Local: td_izq[n]
        # -Resultado: td_izq[n+1]
        td_izq = [pq(elem) for elem in html('td.equipoizquierda')]

        # td.equipoderecha matchea el equipo visitante de cada partido
        td_der = [pq(elem) for elem in html('td.equipoderecha')]

        # Los partidos aún no empezados no tienen un td.equipoizquierda
        # con el resultado. Eso nos sirve para calcular la cantidad
        # de partidos en juego o terminados.
        partidos_empezados = len(td_izq) - 10
        resultados = []

        # Primero, los partidos que tienen resultado
        for x in range(partidos_empezados):
            goles_local, goles_visitante = map(
                int, td_izq[x * 2 + 1].text().split('-'))
            resultados.append({'equipo_local': td_izq[x * 2].text(),
                               'equipo_visitante': td_der[x].text(),
                               'goles_local': goles_local,
                               'goles_visitante': goles_visitante,
                               'estado': self._get_estado_partido(td_izq[x * 2 + 1])})

        # Después, los que no
        for x in range(partidos_empezados, 10):
            indice_izq = x + partidos_empezados
            resultados.append({'equipo_local': td_izq[indice_izq].text(),
                               'equipo_visitante': td_der[x].text(),
                               'goles_local': 0,
                               'goles_visitante': 0,
                               'estado': EstadoPartido.NO_EMPEZADO})

        return resultados

    def _get_estado_partido(self, elem):
        ''' Usa la url de la imagen para determinar el estado del partido. '''
        src = elem('img').attr('src')
        if 'partidoterminado' in src:
            return EstadoPartido.TERMINADO
        elif 'partidoenjuego' in src:
            return EstadoPartido.EN_JUEGO
        return EstadoPartido.NO_EMPEZADO

    def get_equipos(self):
        target_url = self.EQUIPOS_URL.format(camp=self.camp_id)
        html = pq(target_url)
        tabla_equipos = html('td[colspan="20"]').parent().parent()
        lista_equipos = pq(tabla_equipos('tr')[1]).contents()
        escudos = [pq(elem)('a')('img') for elem in lista_equipos]

        return [{'nombre': equipo.attr('alt'),
                 'escudo_url': urljoin(self.EQUIPOS_URL, equipo.attr('src'))}
                for equipo in escudos]
