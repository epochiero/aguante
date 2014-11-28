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

        for x in range(len(td_der)):
            print(td_izq[x * 2]('img')[0].attrib['src'])
            print(td_der[x]('img')[0].attrib['src'])
            print(td_izq[x * 2].text() + " " +
                  td_izq[x * 2 + 1].text() + " " + td_der[x].text())

    def get_equipos(self):
        target_url = self.EQUIPOS_URL.format(camp=self.camp_id)
        html = pq(target_url)
        tabla_equipos = html('td[colspan="20"]').parent().parent()
        lista_equipos = pq(tabla_equipos('tr')[1]).contents()
        escudos = [pq(elem)('a')('img') for elem in lista_equipos]

        return [{'nombre': equipo.attr('alt'),
                 'escudo_url': urljoin(self.EQUIPOS_URL, equipo.attr('src'))}
                for equipo in escudos]
