from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import core
from .constants import *


class ModuloManager(models.Manager):
    def modulos_por_usuario(self, user):
        return self.model.objects.filter(funcionalidad__grupos__user=user,
                                         estado=COD_ITC_ACTIVO).order_by('orden').distinct()


class FuncionalidadManager(models.Manager):
    def funcionalidades_por_usuario(self, user):
        return self.model.objects.filter(grupos__user=user).order_by('orden, modulo__id')

    def funcionalidades_por_modulo(self, modulo, user):
        return self.model.objects.filter(modulo=modulo, grupos__user=user,
                                         estado=COD_ITC_ACTIVO).order_by('orden').distinct()


class ItemManager(models.Manager):
    def items_por_catalogo_id(self, catalogo_id):
        return self.model.objects.filter(catalogo__id=catalogo_id)

    def item_por_codigo_y_por_catalago(self, item_codigo, catalogo_codigo):
        return self.model.objects.get(codigo=item_codigo, catalogo__codigo=catalogo_codigo)

    def items_por_catalogo_cod(self, catalogo_codigo):
        return self.model.objects.filter(catalogo__codigo=catalogo_codigo)

    def item_por_item_cod(self, catalogo_codigo, item_codigo):
        try:
            return self.model.objects.get(catalogo__codigo=catalogo_codigo, codigo=item_codigo)
        except ObjectDoesNotExist:
            return None

    def items_por_item_padre_id(self, item_id):
        return self.model.objects.filter(padre__id=item_id)

    def items_nacionalidad(self):
        return self.model.objects.filter(catalogo__codigo=COD_CAT_NACIONALIDAD)

    def items_estado_civil(self):
        return self.model.objects.filter(catalogo__codigo=COD_CAT_ESTADO_CIVIL)

    def items_genero(self):
        return self.model.objects.filter(catalogo__codigo=COD_CAT_GENERO)

    def masculino(self):
        return self.model.objects.get(catalogo__codigo=COD_CAT_GENERO, codigo=COD_ITC_MASCULINO)

    def femenino(self):
        try:
            return self.model.objects.get(catalogo__codigo=COD_CAT_GENERO, codigo=COD_ITC_FEMENINO)
        except ObjectDoesNotExist:
            return self.model.objects.None()

    def soltero(self):
        return self.model.objects.get(catalogo__codigo=COD_CAT_ESTADO_CIVIL, codigo=COD_ITC_SOLTERO)

    def casado(self):
        return self.model.objects.get(catalogo__codigo=COD_CAT_ESTADO_CIVIL, codigo=COD_ITC_CASADO)

    def viudo(self):
        return self.model.objects.get(catalogo__codigo=COD_CAT_ESTADO_CIVIL, codigo=COD_ITC_VIUDO)

    def provincias(self):
        return self.model.objects.filter(catalogo__codigo=COD_CAT_PROVINCIA)

    def cantones(self):
        return self.model.objects.filter(catalogo__codigo=COD_CAT_CANTON).order_by('nombre')

    def parroquias(self):
        return self.model.objects.filter(catalogo__codigo=COD_CAT_PARROQUIA)


