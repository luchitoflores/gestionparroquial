from core.filters import ItemFilter
from rest_framework.response import Response
from rest_framework import status

__author__ = 'LFL'

from rest_framework import serializers, viewsets, filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Catalogo, Item, Parametro


class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo
        #fields = ['id', 'oferente', 'intencion', 'ofrenda', 'fecha', 'hora', 'parroquia', 'iglesia', 'individual']

    # def validate_nombre(self, value):
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("Blog post is not about Django")
    #     return value

class CatalogoViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogoSerializer
    queryset = Catalogo.objects.all()

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        #fields = ['id', 'oferente', 'intencion', 'ofrenda', 'fecha', 'hora', 'parroquia', 'iglesia', 'individual']


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    #filter_fields = ('codigo',)
    filter_class = ItemFilter

    def get_queryset(self):
        query = self.request.QUERY_PARAMS
        print query
        if 'catalogo' in query.keys():
            return self.queryset
        else:
            return self.queryset.none()

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
