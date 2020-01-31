#-*- coding: utf-8 -*-
from common.models import EstadoPartido
from pyquery import PyQuery as pq
from urllib.parse import urljoin

__all__ = ['UniversoFutbolCrawler']


class UniversoFutbolCrawler():

    """ Recupera resultados y equipos para un torneo. """

    FECHA_URL = "http://www.universofutbol.com/plantillas/archivos/fecha_argentina.php?div=1&camp={camp}&fecha={fecha}"
    TORNEO_URL = "http://www.universofutbol.com/plantillas/archivos/noticias.php?div=1&camp={camp}"

    def __init__(self, camp_id):
        self.camp_id = camp_id

    def get_fecha(self, nro_fecha):
        target_url = self.FECHA_URL.format(camp=self.camp_id, fecha=nro_fecha)
        html = pq(target_url)

        # los <tr> correspondientes a un partido tienen por lo menos un
        # td.equipoizquierda como hijo
        # no puede usarse set() porque las instancias de PyQuery no son
        # hashables (ej. pq(elem))
        filas_partido = []
        for elem in html('td.equipoizquierda'):
            fila = pq(elem).parent()[0]
            if fila not in filas_partido:
                filas_partido.append(fila)

        resultados = []
        for fila_partido in filas_partido:
            resultados.append(self._procesar_partido(fila_partido))

        return resultados

    def _procesar_partido(self, fila_partido):
        td_izq = pq(fila_partido)('td.equipoizquierda')
        td_der = pq(fila_partido)('td.equipoderecha')
        if len(td_izq) == 2:
            # El partido está empezado o terminado
            goles_local, goles_visitante = map(
                int, pq(td_izq[1]).text().split('-'))
            return {'equipo_local': pq(td_izq[0]).text(),
                    'equipo_visitante': pq(td_der[0]).text(),
                    'goles_local': goles_local,
                    'goles_visitante': goles_visitante,
                    'estado': self._get_estado_partido(pq(td_izq[1]))}
        else:
            # El partido aún no empezó
            return {'equipo_local': pq(td_izq[0]).text(),
                    'equipo_visitante': pq(td_der[0]).text(),
                    'goles_local': 0,
                    'goles_visitante': 0,
                    'estado': EstadoPartido.NO_EMPEZADO}

    def _get_estado_partido(self, elem):
        ''' Usa la url de la imagen para determinar el estado del partido. '''
        src = elem('img').attr('src')
        if 'partidoterminado' in src:
            return EstadoPartido.TERMINADO
        elif 'partidoenjuego' in src:
            return EstadoPartido.EN_JUEGO
        return EstadoPartido.NO_EMPEZADO

    def get_equipos(self):
        target_url = self.TORNEO_URL.format(camp=self.camp_id)
        html = pq(target_url)
        tabla_equipos = html('td[colspan="20"]').parent().parent()
        if not tabla_equipos:
            # Hack para manejar el Torneo de los 30 (id=945)
            tabla_equipos = html('td[colspan="30"]').parent().parent()
            lista_equipos = []
            # 3 filas de equipos
            for i in range(1, 4):
                lista_equipos.extend(pq(tabla_equipos('tr')[i]).contents())
        else:
            lista_equipos = pq(tabla_equipos('tr')[1]).contents()
        escudos = [pq(elem)('a')('img') for elem in lista_equipos]

        return [{'nombre': equipo.attr('alt'),
                 'escudo_url': urljoin(self.TORNEO_URL, equipo.attr('src'))}
                for equipo in escudos]

    def get_cantidad_fechas(self):
        target_url = self.TORNEO_URL.format(camp=self.camp_id)
        html = pq(target_url)
        tabla_fechas = html("p:contains('Fecha x Fecha')").parent()
        # Cada <td> es una fecha
        td_fechas = pq(tabla_fechas)('td')
        return len(td_fechas)
