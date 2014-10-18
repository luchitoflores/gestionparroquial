from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import core.models


class FuncionalidadManager(models.Manager):
    def FuncionalidadesPorUsuario(self, user):
        return self.model.objects.filter(grupos__user=user).order_by('orden, modulo__id')

    def FuncionalidadesPorModulo(self, modulo, user):
        return self.model.objects.filter(modulo=modulo, grupos__user=user, estado=True).order_by('orden', 'modulo__id')


class ItemManager(models.Manager):
    def ItemsPorCatalogoId(self, catalogo_id):
        return self.model.objects.filter(catalogo__id=catalogo_id)

    def ItemsPorCatalogoCodigo(self, catalogo_codigo):
        return self.model.objects.filter(catalogo__codigo=catalogo_codigo)

    def ItemPorItemCodigo(self, catalogo_codigo, item_codigo):
        try:
            return self.model.objects.get(catalogo__codigo = catalogo_codigo,codigo=item_codigo)
        except:
            return None

    def ItemsPorItemPadreId(self, item_id):
        return self.model.objects.filter(padre__id=item_id)

class ModuloManager(models.Manager):
    def ModulosPorUsuario(self, user):
        return self.model.objects.filter(funcionalidad__grupos__user=user,
                                         estado=core.models.Item.objects.get(codigo='A')).order_by('id').distinct()
