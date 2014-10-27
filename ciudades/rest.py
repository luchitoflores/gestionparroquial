# -*- coding:utf-8 -*-
import json
# from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ciudades.models import (
    Provincia, Canton, Parroquia
)
from ciudades.forms import DireccionForm
from core.models import Item


class ProvinciaCreateRead(ListCreateAPIView):
    model = Provincia


class ProvinciaCreateReadUpdateDelete(ListCreateAPIView):
    model = Provincia


class CantonCreateRead(ListCreateAPIView):
    model = Canton


class CantonCreateReadUpdateDelete(ListCreateAPIView):
    model = Canton


class ParroquiaCreateRead(ListCreateAPIView):
    model = Parroquia


class ParroquiaCreateReadUpdateDelete(ListCreateAPIView):
    model = Parroquia


def seleccionar_ciudades(request):
    form_direccion = DireccionForm()
    provincia = request.GET.get('provincia')
    canton = request.GET.get('canton')
    lista = list()
    if request.is_ajax():
        if request.method == 'GET':
            if request.GET.get('provincia'):
                cantones = Item.objects.cantones().filter(padre=provincia)
                lista.append({'option': u'<option value="">--Seleccione--</option>'})
                for canton in cantones:
                    lista.append({'option': u'<option value="%s">%s</option>' % (canton.id, canton.nombre)})
                ctx = {'cantones': lista}
                return HttpResponse(json.dumps(ctx), content_type='application/json')

            if request.GET.get('canton'):
                parroquias = Item.objects.parroquias().filter(padre=canton)
                lista.append({'option': u'<option value="">--Seleccione--</option>'})
                for parroquia in parroquias:
                    lista.append({'option': u'<option value="%s">%s</option>' % (parroquia.id, parroquia.nombre)})
                ctx = {'parroquias': lista}
                return HttpResponse(json.dumps(ctx), content_type='application/json')


def direccion_create_view(request):
    if request.is_ajax():
        if request.method == 'POST':
            respuesta = False
            form_direccion = DireccionForm(request.POST)
            if form_direccion.is_valid():
                respuesta = True
                form_direccion.save()
                ctx = {'respuesta': respuesta}
                return HttpResponse(json.dumps(ctx), content_type='application/json')
            else:
                respuesta = False
                ctx = {'respuesta': respuesta, 'errores': form_direccion.errors}
                return HttpResponse(json.dumps(ctx), content_type='application/json')

            # else:


	