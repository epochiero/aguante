from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.views.generic.base import View

from pronosticos.models import Equipo, Fecha, Torneo


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
        fecha = self.kwargs.get('fecha', Torneo.objects.all()[0].get_fecha_activa())
        context = super().get_context_data(**kwargs)
        if fecha:
            fecha = fecha.numero
            context['partidos'] = Fecha.objects.get(
                numero=fecha, torneo=Torneo.objects.all()[0]).get_partidos()
            context['fecha'] = fecha

        return context
