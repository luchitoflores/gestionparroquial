# -*- coding:utf-8 -*-
from django.forms.widgets import CheckboxSelectMultiple
from django.db import models
from core.models import Item

# Create your models here.

class Provincia(models.Model):
    nombre = models.CharField('Nombre *', max_length=50, help_text='Ingrese el nombre de una Provincia Ej: Loja.'
                                                                   + ' El Oro')
    abreviatura = models.CharField('Código *', unique=True, max_length=4,
                                   help_text='Ingrese una abreviatura para la Provincia' +
                                             ' Ej: LO')

    class Meta:
        verbose_name = u'Provincia'
        verbose_name_plural = u'Provincias'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return '/ciudades/provincia/%i' % (self.id)


class Canton(models.Model):
    nombre = models.CharField('Nombre *', max_length=50, help_text='Ingrese un Canton Ej: Espíndola, Calvas')
    abreviatura = models.CharField('Código *', unique=True, max_length=4,
                                   help_text='Ingrese una abreviatura Ej:lo, Ca, A')
    provincia = models.ForeignKey(Provincia, verbose_name=u'Provincia *', related_name='provincia')

    class Meta:
        verbose_name = u'Cantón'
        verbose_name_plural = u'Cantones'
        ordering = ['nombre', 'provincia__nombre']

    def __unicode__(self):
        return u'%s - %s' % (self.nombre, self.provincia.nombre)

    def get_absolute_url(self):
        return '/ciudades/canton/%i' % (self.id)


class Parroquia(models.Model):
    nombre = models.CharField('Nombre *', max_length=50, help_text='Ingrese Parroquia Ej: Catamayo, Cariamanga')
    abreviatura = models.CharField('Código *', unique=True, max_length=4,
                                   help_text='Ingrese una abreviatura Ej:ca, C-a')
    canton = models.ForeignKey(Canton, verbose_name=u'Cantón *', related_name='canton')

    class Meta:
        verbose_name = u'Parroquia Civil'
        verbose_name_plural = u'Prarroquias Civiles'
        ordering = ['nombre', 'canton__nombre']

    def __unicode__(self):
        return u'%s - %s' % (self.nombre, self.canton.nombre)

    def get_absolute_url(self):
        return '/ciudades/parroquia/%i' % (self.id)


class Direccion(models.Model):
    domicilio = models.CharField('Calles *', max_length=100,
                                 help_text='Ingrese las calles. Ej: 10 agosto 10-04, Bernardo Valdivieso')
    provincia = models.ForeignKey(Item, related_name=u'direccion_provincia')
    canton = models.ForeignKey(Item, related_name=u'direccion_canton')
    parroquia = models.ForeignKey(Item, related_name=u'direccion_parroquia')
    telefono = models.CharField('Teléfono', max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = u'Dirección'
        verbose_name_plural = u'Direcciones'
        ordering = ['provincia__nombre', 'canton__nombre', 'parroquia__nombre']

    def __unicode__(self):
        return u'%s' % (self.domicilio)

