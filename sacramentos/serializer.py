# -*- coding:utf-8 -*-
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework import serializers, viewsets, filters, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Intencion, PerfilUsuario
from sacramentos.models import Agenda
import locale
locale.setlocale(locale.LC_ALL, '')

class IntencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intencion
        fields = ['id', 'oferente', 'intencion', 'ofrenda', 'fecha', 'hora', 'parroquia', 'iglesia', 'individual']


class IntencionViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = IntencionSerializer
    queryset = Intencion.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id',)


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        #fields = ('dni',)


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = PerfilUsuarioSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('dni',)
    queryset = PerfilUsuario.objects.all()

class AgendaSerializer(serializers.ModelSerializer):
    textoCabeceraAgenda = serializers.SerializerMethodField('get_x')

    def get_x(self, instance):
        return self.context['textoCabeceraAgenda']

    class Meta:
        model = Agenda

class AgendaListAPIView(APIView):
    def get(self, request, format=None):
        agenda = list()
        textoCabeceraAgenda = ''
        fecha = self.request.QUERY_PARAMS.get('fecha', '')
        rango = self.request.QUERY_PARAMS.get('rango', '')
        contador = self.request.QUERY_PARAMS.get('contador', '')

        queryset = Agenda.objects.none()

        if fecha and rango and contador:
            currentdate = datetime.datetime.strptime(fecha, "%Y-%m-%d")
            contador = int(contador)
            queryset = Agenda.objects.filter(fecha=currentdate)
            if rango == 'dia':
                currentdate.strftime('%A')
                if contador:
                    dias = timedelta(days=int(contador))
                    currentdate = currentdate + dias

                for evento in Agenda.objects.filter(fecha=currentdate).order_by('fecha', 'hora'):
                    evnt = dict()
                    evnt['evento'] = evento.evento
                    evnt['fecha'] = evento.fecha
                    evnt['hora'] = evento.hora
                    evnt['id'] = evento.id
                    agenda.append(evnt)
                textoCabeceraAgenda = currentdate.date()

            elif rango == 'semana':
                currentdate.strftime('%w')
                if contador:
                    dias = timedelta(weeks=contador)
                    currentdate = currentdate + dias
                start = currentdate - timedelta(days = currentdate.weekday())
                end = start + timedelta(days=6)

                for evento in Agenda.objects.filter(fecha__range=[start, end]).order_by('fecha', 'hora'):
                    evnt = dict()
                    evnt['fecha'] = evento.fecha
                    evnt['hora'] = evento.hora
                    evnt['evento'] = evento.evento
                    evnt['id'] = evento.id
                    agenda.append(evnt)

                textoCabeceraAgenda = u'%s - %s' % (start.date(), end.date())

            elif rango == 'mes':
                if contador != 0:
                    #month_to_add =
                    currentdate = currentdate + relativedelta(months=contador)


                for evento in Agenda.objects.filter(fecha__month=currentdate.strftime('%m'), fecha__year=currentdate.year).order_by('fecha', 'hora'):
                    evnt = dict()
                    evnt['fecha'] = evento.fecha
                    evnt['hora'] = evento.hora
                    evnt['evento'] = evento.evento
                    evnt['id'] = evento.id
                    agenda.append(evnt)

                textoCabeceraAgenda = u'%s - %s' % (currentdate.strftime('%B'), currentdate.year)

        ctx = {'agenda': agenda, "textoCabeceraAgenda": textoCabeceraAgenda}
        return Response(ctx)

class AgendaListaaaaAPIView(generics.ListAPIView):
    serializer_class = AgendaSerializer

    def get_serializer_context(self):
        context = super(AgendaListAPIView, self).get_serializer_context()
        fecha = self.request.QUERY_PARAMS.get('fecha', '')
        rango = self.request.QUERY_PARAMS.get('rango', '')
        contador = self.request.QUERY_PARAMS.get('contador', '')
        textoCabeceraAgenda = ""
        if fecha and rango and contador:
            currentdate = datetime.datetime.strptime(fecha, "%Y-%m-%d")
            contador = int(contador)
            queryset = Agenda.objects.filter(fecha=currentdate)
            if rango == 'dia':
                currentdate.strftime('%A')
                if contador:
                    dias = timedelta(days=int(contador))
                    currentdate = currentdate + dias

                textoCabeceraAgenda = currentdate
            elif rango == 'semana':
                currentdate.strftime('%w')
                if contador:
                    dias = timedelta(days=int(contador))
                    currentdate = currentdate + dias + 7
                start = currentdate - timedelta(days = currentdate.weekday())
                end = start + timedelta(days = 6)
                textoCabeceraAgenda = u'%s - %s' % (start, end)
            elif rango == 'mes':
                if contador != 0:
                    #month_to_add =
                    currentdate = currentdate + relativedelta(months=contador)
                    currentdate.strftime('%B')
                textoCabeceraAgenda = currentdate

        context.update({'textoCabeceraAgenda': textoCabeceraAgenda})
        return context

    # def __init__(self, *args, **kwargs):
    #     self = kwargs.pop('prueba', None)
    #     super(AgendaListAPIView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        fecha = self.request.QUERY_PARAMS.get('fecha', '')
        rango = self.request.QUERY_PARAMS.get('rango', '')
        contador = self.request.QUERY_PARAMS.get('contador', '')
        queryset = Agenda.objects.all()

        if fecha and rango and contador:
            currentdate = datetime.datetime.strptime(fecha, "%Y-%m-%d")
            contador = int(contador)
            queryset = Agenda.objects.filter(fecha=currentdate)
            if rango == 'dia':
                currentdate.strftime('%A')
                if contador:
                    dias = timedelta(days=int(contador))
                    currentdate = currentdate + dias
                return Agenda.objects.filter(fecha=currentdate)
            elif rango == 'semana':
                currentdate.strftime('%w')
                if contador:
                    dias = timedelta(days=int(contador))
                    currentdate = currentdate + dias + 7
                start = currentdate - timedelta(days = currentdate.weekday())
                end = start + timedelta(days = 6)
                return Agenda.objects.filter(fecha__range=[start, end])
            elif rango == 'mes':
                if contador != 0:
                    #month_to_add =
                    currentdate = currentdate + relativedelta(months=contador)
                currentdate.strftime('%B')
                return Agenda.objects.filter(fecha__month=currentdate.strftime('%m'))
        return queryset






