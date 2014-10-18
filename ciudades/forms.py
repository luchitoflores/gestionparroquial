# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import *
from .models import Provincia, Canton, Parroquia, Direccion
class ProvinciaForm(ModelForm):
	class Meta:
		model = Provincia
		widgets = {
		'nombre': forms.TextInput(attrs={'required':''}),
		'abreviatura': forms.TextInput(attrs={'required':''})
		}
class CantonForm(ModelForm):
	class Meta:
		model = Canton
		widgets = {
		'nombre': forms.TextInput(attrs={'required':''}),
		'abreviatura': forms.TextInput(attrs={'required':''}),
		'provincia': forms.TextInput(attrs={'required':''})
		}
	def __init__(self, *args, **kwargs):
		super(CantonForm, self).__init__(*args, **kwargs)
		self.fields['provincia'].empty_label='-- Seleccione --'

class ParroquiaForm(ModelForm):
	class Meta:
		model = Parroquia
		fields = ('nombre','abreviatura','canton')
		widgets = {
		'nombre': forms.TextInput(attrs={'required':''}),
		'abreviatura': forms.TextInput(attrs={'required':''}),
		'canton': forms.TextInput(attrs={'required':''})
		}

	def __init__(self, *args, **kwargs):
		super(ParroquiaForm, self).__init__(*args, **kwargs)
		self.fields['canton'].empty_label='-- Seleccione --'

# Forms para dirección
class DireccionForm(ModelForm):
	class Meta:
		model = Direccion
		fields = ('domicilio','provincia', 'canton','parroquia', 'telefono')
		widgets = {
		'domicilio': forms.TextInput(attrs={'required':''}),
		'provincia': forms.Select(attrs={'required':''}),
		'canton': forms.Select(attrs={'required':'', 'disabled':''}),
		'parroquia': forms.Select(attrs={'required':'', 'disabled':''}),
		}

	def __init__(self, *args, **kwargs):
		super(DireccionForm, self).__init__(*args, **kwargs)
		self.fields['provincia'].empty_label = '-- Seleccione --'
		self.fields['provincia'].queryset = Provincia.objects.all()
		self.fields['canton'].queryset = Canton.objects.none()
		self.fields['canton'].empty_label = '-- Seleccione --'
		self.fields['parroquia'].queryset = Parroquia.objects.none()
		self.fields['parroquia'].empty_label = '-- Seleccione --'  		
 
