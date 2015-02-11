__author__ = 'sistemas'

import django_filters
from .models import Catalogo, Item

class ItemFilter(django_filters.FilterSet):
    catalogo = django_filters.CharFilter(name='catalogo__codigo')
    class Meta:
        model = Item
        fields = ('catalogo',)

