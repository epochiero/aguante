from .models import Equipo, Fecha, Partido, Torneo
from rest_framework import serializers


class EquipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipo
        fields = ('nombre', 'escudo')


class FechaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fecha
        #fields = ('nombre', 'escudo')


class PartidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partido
        #fields = ('nombre', 'escudo')


class TorneoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Torneo
        #fields = ('nombre', 'escudo')
