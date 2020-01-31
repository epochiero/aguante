from .models import Fecha, Partido
from .serializers import FechaSerializer, PartidoSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class FechaViewSet(ReadOnlyModelViewSet):
    queryset = Fecha.objects.all()
    serializer_class = FechaSerializer


class PartidoViewSet(ReadOnlyModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
