from django.contrib import admin
from futbol.models import Equipo, Fecha, Partido, Torneo

admin.site.register(Equipo)
admin.site.register(Fecha)
admin.site.register(Partido)


def admin_cargar_equipos(modeladmin, request, queryset):
    for torneo in queryset:
        torneo.cargar_equipos()
admin_cargar_equipos.short_description = "Cargar equipos del torneo"


def admin_cargar_fechas(modeladmin, request, queryset):
    for torneo in queryset:
        torneo.cargar_fechas()
admin_cargar_fechas.short_description = "Cargar fechas del torneo"


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    exclude = ('equipos_cargados', 'cantidad_fechas',)
    actions = (admin_cargar_equipos, admin_cargar_fechas,)
