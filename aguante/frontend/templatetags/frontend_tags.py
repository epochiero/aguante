from common.models import EstadoPartido
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def icono_estado(partido):
    if partido.estado == EstadoPartido.NO_EMPEZADO:
        return "noempezado"
    elif partido.estado == EstadoPartido.EN_JUEGO:
        return "enjuego"
    return "terminado"
