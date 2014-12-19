from __future__ import absolute_import

from celery import Task

from crawlers.crawlers import UniversoFutbolCrawler


class ActualizarPartidosTask(Task):

    def __init__(self, camp_id):
        self.crawler = UniversoFutbolCrawler(camp_id)

    def run(self, fecha):
        partidos = self.crawler.get_fecha(fecha)

