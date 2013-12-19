# -*- coding:utf-8 -*-
from django.forms.widgets import CheckboxSelectMultiple
from django.db import models

# Create your models here.

class Provincia(models.Model):
	nombre=models.CharField(max_length=100,help_text='Ingrese el nombre de una Provincia Ej: Loja,'
		+' El Oro')
	abreviatura=models.CharField('Código', unique=True,  max_length=2,help_text='Ingrese una abreviatura para la Provincia'+
		' Ej:lo, el, p')


	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return '/ciudades/provincia/%i' %(self.id)

	class Meta:
		ordering = ('nombre',)


class Canton(models.Model):
	nombre=models.CharField(max_length=100,help_text='Ingrese un Canton Ej: Espíndola, Calvas')
	abreviatura=models.CharField('Código',  unique=True,  max_length=4, help_text='Ingrese una abreviatura Ej:lo, Ca, A')
	provincia=models.ForeignKey(Provincia, related_name='provincia')


	def __unicode__(self):
		return u'%s - %s' % (self.nombre, self.provincia.nombre)

	def get_absolute_url(self):
		return '/ciudades/canton/%i' %(self.id)

	class Meta:
		ordering = ('nombre',)

class Parroquia(models.Model):
	nombre=models.CharField(max_length=100,help_text='Ingrese Parroquia Ej: Catamayo, Cariamanga')
	abreviatura=models.CharField('Código',  unique=True, max_length=6, help_text='Ingrese una abreviatura Ej:ca, C-a')
	canton=models.ForeignKey(Canton, related_name='canton')
	def __unicode__(self):
		return u'%s - %s' % (self.nombre, self.canton.nombre)

	def get_absolute_url(self):
		return '/ciudades/parroquia/%i' %(self.id)

	class Meta:
		ordering = ('nombre',)


class Direccion(models.Model):
	domicilio=models.CharField('Domicilio', max_length=200)
	provincia=models.ForeignKey(Provincia)
	canton=models.ForeignKey(Canton)
	parroquia=models.ForeignKey(Parroquia, related_name='parroquia_civil')
	telefono=models.CharField(max_length=10, blank=True, null=True)
	

	def __unicode__(self):
		return u'%s' % (self.domicilio)

