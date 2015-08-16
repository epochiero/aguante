from common.models import EstadoPartido
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def icono_estado(partido):
    """Devuelve un <div> con el icono de estado del partido"""
    estado = "terminado"
    if partido.estado == EstadoPartido.NO_EMPEZADO:
        estado = "noempezado"
    elif partido.estado == EstadoPartido.EN_JUEGO:
        estado = "enjuego"
    return mark_safe('<div class="icono-estado icono-estado-{}"></div>'.format(estado))
