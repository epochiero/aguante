from django.contrib import admin
from pronosticos.models import Equipo, Fecha, Partido, Pronostico, Torneo

admin.site.register(Equipo)
admin.site.register(Fecha)
admin.site.register(Partido)
admin.site.register(Pronostico)
admin.site.register(Torneo)
