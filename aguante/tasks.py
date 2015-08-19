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
                    .format(torneo_activo.id))
        return

    logger.info("Actualizando partidos, {}".format(fecha_activa))
    fecha_activa.actualizar_partidos()
