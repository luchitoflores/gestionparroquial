# -*- coding:utf-8 -*-
from rest_framework import serializers, viewsets, filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Intencion

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




