__author__ = 'sistemas'

import django_filters
import datetime
from datetime import date
from .models import Catalogo, Item, Funcionalidad
from django.contrib.admin.models import LogEntry


class CatalogoFilter(django_filters.FilterSet):
    catalogoPadre = django_filters.CharFilter(name='catalogo__codigo')

    class Meta:
        model = Item
        fields = ('catalogo',)


class ItemFilter(django_filters.FilterSet):
    catalogo = django_filters.CharFilter(name='catalogo__codigo')

    class Meta:
        model = Item
        fields = ('catalogo',)

class ItemsPadreFilter(django_filters.FilterSet):
    catalogo = django_filters.CharFilter(name='catalogo__codigo')
    catalogoPadre = django_filters.CharFilter(name='catalogo__padre__id')
    class Meta:
        model = Item
        fields = ('catalogo', 'padre', 'catalogoPadre',)


class LogEntryFilter(django_filters.FilterSet):
    fechaFinal = django_filters.MethodFilter(action="filter_date_end", required=True)
    fechaInicial = django_filters.MethodFilter(action="filter_date_start", required=True)

    class Meta:
        model = LogEntry
        fields = ('user', 'action_flag', 'fechaInicial', 'fechaFinal')

    @staticmethod
    def filter_date_start(queryset, value):
        currentdate = datetime.datetime.strptime(value, "%d/%m/%Y")
        currentdatetime = datetime.datetime.combine(currentdate, datetime.time.min)
        return queryset.filter(action_time__gt=currentdatetime)

    @staticmethod
    def filter_date_end(queryset, value):
        currentdate = datetime.datetime.strptime(value, "%d/%m/%Y")
        currentdatetime = datetime.datetime.combine(currentdate, datetime.time.max)
        #raise ValueError('dsdd')
        return queryset.filter(action_time__lt=currentdatetime)



class FuncionalidadFilter(django_filters.FilterSet):
    modulo = django_filters.CharFilter(name='modulo__codigo')

    class Meta:
        model = Funcionalidad
        fields = ('modulo',)

