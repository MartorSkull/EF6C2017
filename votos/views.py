# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from votos.models import *


def resultado_global(request):
    """
    Generar la vista para devolver el resultado global de la elección.
    Tener en cuenta que tiene que tener:
    Cantidad total de votos por candidato
    Cantidad total de votos nulos
    Porcentaje de cada candidato
    Porcentaje de votos nulos
    Total de votos de la elección
    """
    totalVotantes=Votos.objects.all().count()
    # for i in Distrito.objects.all():
    #     totalVotantes=i.cantidad_votantes
    context={
        'orderedCandidates': sorted(Candidato.objects.all(), key=lambda t: t.voted(), reverse=True),
        'blankVotes': float((Votos.objects.filter(voted=None).count()*100))/totalVotantes,
    }
    context['distritos'] = Distrito.objects.all()
    return render(request,'global.html',context)


def resultado_distrital(request, distId):
    """
    Generar la vista para devolver el resultado distrital de la elección
    Tener en cuenta que tiene que tener:
    Tamaño del padrón
    Porcentaje de votos del distrito (respecto al padron. Ejemplo: Si el distrito tiene 1000 votantes y hay 750 votos, el porcentaje es 75%)
    Total de votos del distrito
    Candidato ganador
    """
    try:
        distrito=Distrito.objects.get(pk=distId)
    except ObjectDoesNotExist:
        return HttpResponse(404)
    votos=Votos.objects.filter(district=distrito).count()
    ganador = sorted(Candidato.objects.all(), key=lambda o: o.votedIn(distrito.id), reverse=True)[0]
    context={
        'distrito': distrito,
        'porcentaje_votantes': float((votos*100))/distrito.cantidad_votantes,
        'total_votantes': votos,
        'ganador': ganador
    }

    return render(request,'distrital.html',context)
