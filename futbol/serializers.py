from .models import Fecha, Partido
from rest_framework import serializers


class PartidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partido
        fields = ('id', 'goles_local', 'goles_visitante', 'estado')


class FechaSerializer(serializers.ModelSerializer):
    partidos = PartidoSerializer(many=True)

    class Meta:
        model = Fecha
        fields = ('id', 'numero', 'terminada', 'partidos')
