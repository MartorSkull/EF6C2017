# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Distrito(models.Model):
    """
    Se decide utilizar este modelo para la clase distrito porque es
    necesario el nombre y la cantidad de votantes,
    y en un futuro se mostrara un mapa con un marker por cada distrito
    que contenga los resultados del mismo.
    """
    nombre = models.CharField('Nombre del distrito', max_length=128)
    cantidad_votantes = models.IntegerField('Cantidad de votantes', default=0)
    latitude = models.DecimalField('Latitud', max_digits=14, decimal_places=10, default=0)
    longitude = models.DecimalField('Latitud', max_digits=14, decimal_places=10, default=0)


    def __str__(self):
        return 'Distrito {}'.format(self.nombre)

class Candidato(models.Model):
    """
    Ese modelo ha sido diseniado con la idea de que se necesitara:
    el nombre del Candidato y el apellido del mismo.
    Entre los metodos de este modelo encontramos:
    fullname: genera el nombre completo del candidato
    percent: calcula el porcentaje global del candidato
    percentIn: calcula el porcentaje dentro de un distrito
    voted: la cantidad de votos que recibio el candidato
    votedIn: la cantidad de votos que recibio un candidato en un distrito
    De esta forma la mayor parte de los calculos se realizan directamente desde 
    Lo cual permite acceder mas facil a los datos.
    """
    nombre = models.CharField(max_length=128)
    apellido = models.CharField(max_length=128)

    def fullname(self):
        return "{}, {}".format(self.apellido, self.nombre)

    def percent(self):
        total = Votos.objects.all().count()
        #for distrito in Distrito.objects.all():
        #    total += distrito.cantidad_votantes

        return float((self.voted()*100))/total

    def percentIn(self, distId):
        distrito = Distrito.objects.get(pk=distId)
        return float((self.votedIn(distrito.id)*100))/Votos.objects.filter(district=distrito, voted=self).count()

    def voted(self):
        return Votos.objects.filter(voted = self).count()

    def votedIn(self, distId):
        district = Distrito.objects.get(pk=distId)
        return Votos.objects.filter(voted=self, district=district).count()

    def __str__(self):
        return self.fullname()

class Votos(models.Model):
    """
    Este modelo ha sido diseniado con la idea de que se necesitara 
    el candidato votado, este puede ser en blanco, guardado en voted 
    y el distrito en el que se realizo este voto para luego obtener las
    estadisticas necesarias para cada distrito
    """
    voted = models.ForeignKey(Candidato, null=True, blank=True)
    district = models.ForeignKey(Distrito)

    def __str__(self):
        return "{} @ {}".format(self.voted, self.district)