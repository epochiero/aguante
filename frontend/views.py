from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.views.generic.base import View

from futbol.models import Equipo, Fecha, Torneo


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipos'] = Equipo.objects.all()
        return context


class LoginView(View):

    def post(self, request, *args, **kwargs):
        user = authenticate(username='john', password='secret')

        return


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        id_torneo = self.kwargs.get('torneo', None)
        nro_fecha = self.kwargs.get('fecha', None)
        context = super().get_context_data(**kwargs)
        if not id_torneo:
            torneo = Torneo.get_activo()
        else:
            torneo = Torneo.objects.get(id=id_torneo)
        context['torneo'] = torneo

        if not nro_fecha:
            context['fecha'] = torneo.get_fecha_activa()
        else:
            context['fecha'] = torneo.fechas.get(numero=nro_fecha)
        context['torneos'] = Torneo.objects.all()
        return context
