from __future__ import absolute_import

from aguante.celeryconfig import app
from celery.utils.log import get_task_logger
from crawlers.crawlers import UniversoFutbolCrawler
from futbol.models import Torneo


logger = get_task_logger(__name__)


@app.task()
def actualizar_partidos():
    """ Tarea para actualizar información de partidos en tiempo real.
        Solamente actualiza info para el torneo activo y la fecha activa
        de ese torneo. """

    torneo_activo = Torneo.get_activo()
    if not torneo_activo:
        logger.info("No hay ningún torneo marcado como activo.")
        return
    fecha_activa = torneo_activo.get_fecha_activa()
    if not fecha_activa:
        logger.info("No hay ninguna fecha marcada como activa para el torneo {}"
                    .format(id_torneo=torneo_activo.id))
        return
    crawler = UniversoFutbolCrawler(
        torneo_activo.universofutbol_id)

    # TODO: no seguir si ya terminaron todos los partidos
    logger.info("Actualizando partidos, fecha {} {}".format(
        fecha_activa.numero, torneo_activo.nombre))
    fecha_activa.actualizar_partidos(crawler)
