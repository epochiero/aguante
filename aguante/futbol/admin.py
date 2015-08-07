from django.contrib import admin
from futbol.models import Equipo, Fecha, Partido, Torneo

admin.site.register(Equipo)
admin.site.register(Fecha)
admin.site.register(Partido)
admin.site.register(Torneo)
