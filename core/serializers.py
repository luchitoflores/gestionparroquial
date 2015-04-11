__author__ = 'LFL'
from django.contrib.auth.models import Group, User, Permission


from rest_framework import serializers, viewsets, filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from core.filters import ItemFilter, FuncionalidadFilter, ItemsPadreFilter
from .models import Catalogo, Item, Parametro, Modulo, Funcionalidad
from .constants import CAT_TRANSACCIONES


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


class CatalogoPadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        fields = ('id', 'nombre', 'codigo', 'descripcion', 'estado', 'padre', 'editable')


class CatalogoSerializer(serializers.ModelSerializer):
    #padre = CatalogoPadreSerializer()
    padreCodigo = serializers.SerializerMethodField('get_padre_codigo')

    class Meta:
        model = Catalogo
        fields = ('id', 'nombre', 'codigo', 'descripcion', 'estado', 'padre', 'padreCodigo', 'editable',)
        extra_kwargs = {'padre': {'prueba': 'nombre'}}
        #read_only_fields = ('codigo',)

    def get_padre_codigo(self, obj):

        if obj.padre is None:
            return None
        else:
            return obj.padre.codigo

    # def validate_nombre(self, value):
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("Blog post is not about Django")
    #     return value



class CatalogoViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogoSerializer
    queryset = Catalogo.objects.all().order_by('nombre')
    ordering = ('nombre', 'codigo')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item

        #fields = ['id', 'oferente', 'intencion', 'ofrenda', 'fecha', 'hora', 'parroquia', 'iglesia', 'individual']


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
    grupos = GroupSerializer(many=True, read_only=True)
    class Meta:
        model = Funcionalidad
        fields = ('id', 'nombre', 'url', 'codigo', 'modulo', 'estado', 'descripcion', 'orden', 'icono', 'grupos')


class FuncionalidadViewSet(viewsets.ModelViewSet):
    serializer_class = FuncionalidadSerializer
    queryset = Funcionalidad.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = FuncionalidadFilter


class LogsSearchSerializer(serializers.ListSerializer):
    usuarios = serializers.ChoiceField(queryset=User.objects.all())
    fecha_inicial = serializers.DateField()
    fecha_final = serializers.DateField()
    transaccion = serializers.ChoiceField(queryset=Item.objects.items_por_catalogo_cod(CAT_TRANSACCIONES))


class LogsSearchViewSet(viewsets.GenericViewSet):
    serializer_class = LogsSearchSerializer





