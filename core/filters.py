__author__ = 'sistemas'

import django_filters
from .models import Catalogo, Item, Funcionalidad

class ItemFilter(django_filters.FilterSet):
    catalogo = django_filters.CharFilter(name='catalogo__codigo')
    class Meta:
        model = Item
        fields = ('catalogo',)


class FuncionalidadFilter(django_filters.FilterSet):
    modulo = django_filters.CharFilter(name='modulo__codigo')
    class Meta:
        model = Funcionalidad
        fields = ('modulo',)

