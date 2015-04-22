from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from core.models import Item


class LibroManager(models.Manager):
    def libro(self):
        return self.model.objects.filter(tipo_libro='Bautismo', estado='Abierto',
                                         parroquia=self.parroquia)

    def ultimo_libro(self, parroquia, tipo_libro):
        try:
            return self.model.objects.filter(parroquia=parroquia, tipo_libro=tipo_libro).latest('created')
        except ObjectDoesNotExist:
            return None


class PersonaManager(models.Manager):
    def padre(self):
        return self.model.objects.filter(sexo=Item.objects.masculino()).exclude(
            user__groups__name='Sacerdote')

    def madre(self):
        return self.model.objects.filter(sexo=Item.objects.femenino())

    def feligres(self):
        return self.model.objects.all().exclude(user__groups__name='Sacerdote')

    def male(self):
        return self.model.objects.filter(sexo=Item.objects.masculino()).exclude(
            user__groups__name='Sacerdote')

    def female(self):
        return self.model.objects.filter(sexo=Item.objects.femenino())

    def todos(self):
        return self.model.objects.all()

    def administrador(self):
        return self.model.objects.filter(user__groups__name='Administrador')

    def sacerdote(self):
        return self.model.objects.filter(user__groups__name='Sacerdote')

    def parroco(self, parroquia):
        return self.model.objects.filter(user__groups__name='Sacerdote', profesion='Sacerdote',
                                         asignacionparroquia__parroquia=parroquia,
                                         asignacionparroquia__periodos__estado=True)

    def username_disponible(self, username):
        try:
            persona = self.model.objects.get(user__username=username)
            return persona.user.username
        except:
            return True


class PeriodoAsignacionManager(models.Manager):
    def secretaria(self, parroquia):
        return self.model.objects.filter(asignacion__persona__user__groups__name='Secretaria',
                                         asignacion__parroquia=parroquia)

