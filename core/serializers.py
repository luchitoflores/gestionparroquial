# -*- coding: utf-8 -*-
__author__ = 'LFL'
from django.contrib.auth.models import Group, User, Permission
from django.contrib.admin.models import LogEntry


from rest_framework import serializers, viewsets, filters, generics
from rest_framework import views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from core.filters import ItemFilter, FuncionalidadFilter, ItemsPadreFilter, LogEntryFilter
from .models import Catalogo, Item, Parametro, Modulo, Funcionalidad
from .constants import COD_CAT_TRANSACCIONES
from rest_framework.decorators import api_view
from rest_framework.response import Response


class GroupSerializer(serializers.ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     many = kwargs.pop('many', True)
    #     super(GroupSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Group
        fields = ('id', 'name',)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission

class PermissionViewSet(viewsets.ModelViewSet):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class CatalogoSerializer(serializers.ModelSerializer):
    padreCodigo = serializers.SerializerMethodField('get_padre_codigo')

    class Meta:
        model = Catalogo
        fields = ('id', 'nombre', 'codigo', 'descripcion', 'estado', 'padre', 'padreCodigo', 'editable',)
        #extra_kwargs = {'padre': {'write_only': True}}
        #read_only_fields = ('codigo',)

    def get_padre_codigo(self, obj):

        if obj.padre is None:
            return None
        else:
            return obj.padre.codigo


class CatalogoViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogoSerializer
    """
    Ordenar ignorando mayúsculas y minúsculas
    """
    queryset = Catalogo.objects.all().extra(select={'lower_nombre': 'lower(nombre)'}).order_by('lower_nombre')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item


class ItemsPaginatedViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all().order_by('nombre')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ItemsPadreFilter
    paginate_by = 10


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all().order_by('nombre')
    filter_backends = (filters.DjangoFilterBackend,)
    #filter_class = ItemFilter
    filter_class = ItemsPadreFilter

    def get_queryset(self):
        query = self.request.QUERY_PARAMS
        print query
        if 'catalogo' in query.keys():
            return self.queryset
        else:
            #return self.queryset.none()
            return self.queryset

    # def list(self, request):
    #     if self.queryset is None:
    #         return Response({"as":"ew"}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         queryset = Item.objects.all()
    #         serializer = ItemSerializer(queryset, many=True)
    #         return Response(serializer.data)


class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro


class ParametroViewSet(viewsets.ModelViewSet):
    serializer_class = ParametroSerializer
    queryset = Parametro.objects.all()


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo


class ModuloViewSet(viewsets.ModelViewSet):
    serializer_class = ModuloSerializer
    queryset = Modulo.objects.all()


class FuncionalidadSerializer(serializers.ModelSerializer):
    #grupos = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Funcionalidad
        fields = ('id', 'nombre', 'url', 'codigo', 'modulo', 'estado', 'descripcion', 'orden', 'icono', 'grupos')


class FuncionalidadViewSet(viewsets.ModelViewSet):
    serializer_class = FuncionalidadSerializer
    queryset = Funcionalidad.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = FuncionalidadFilter


class LogsSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry


class LogsSearchListAPIView(generics.ListAPIView):
    serializer_class = LogsSearchSerializer
    queryset = LogEntry.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = LogEntryFilter
    paginate_by = 10








