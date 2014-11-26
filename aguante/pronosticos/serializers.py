from .models import Equipo, Fecha, Partido, Pronostico, Torneo
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


class PronosticoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pronostico
        #fields = ('nombre', 'escudo')


class TorneoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Torneo
        #fields = ('nombre', 'escudo')
