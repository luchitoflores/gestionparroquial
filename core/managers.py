from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import core.models


class FuncionalidadManager(models.Manager):
    def funcionalidades_por_usuario(self, user):
        return self.model.objects.filter(grupos__user=user).order_by('orden, modulo__id')

    def funcionalidades_por_modulo(self, modulo, user):
        return self.model.objects.filter(modulo=modulo, grupos__user=user, estado=True).order_by('orden', 'modulo__id')


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
        return self.model.objects.filter(catalogo__codigo='NACIONALIDAD')

    def items_estado_civil(self):
        return self.model.objects.filter(catalogo__codigo='EST_CIVIL')

    def items_genero(self):
        return self.model.objects.filter(catalogo__codigo='GEN')

    def masculino(self):
        return self.model.objects.get(catalogo__codigo='GEN', codigo='M')

    def femenino(self):
        try:
            return self.model.objects.get(catalogo__codigo='GEN', codigo='F')
        except ObjectDoesNotExist:
            return self.model.objects.None()

    def soltero(self):
        return self.model.objects.get(catalogo__codigo='EST_CIVIL', codigo='SOLT')

    def casado(self):
        return self.model.objects.get(catalogo__codigo='EST_CIVIL', codigo='CAS')

    def viudo(self):
        return self.model.objects.get(catalogo__codigo='EST_CIVIL', codigo='VIU')

    def provincias(self):
        return self.model.objects.filter(catalogo__codigo='PROVINCIAS')

    def cantones(self):
        return self.model.objects.filter(catalogo__codigo='CANTONES').order_by('nombre')

    def parroquias(self):
        return self.model.objects.filter(catalogo__codigo='PARROQUIAS')




class ModuloManager(models.Manager):
    def ModulosPorUsuario(self, user):
        return self.model.objects.filter(funcionalidad__grupos__user=user,
                                         estado=core.models.Item.objects.get(codigo='A')).order_by('id').distinct()
