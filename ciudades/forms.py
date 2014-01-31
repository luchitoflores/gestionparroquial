# -*- coding:utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.widgets import *
from .models import Provincia, Canton, Parroquia, Direccion


class ProvinciaForm(ModelForm):
	nombre = forms.CharField(max_length=30,required=True, label='Nombre', 
		help_text='Ingrese el nombre de la provincia. Ej: Loja',
		widget=forms.TextInput(attrs={'required': ''}))
	abreviatura = forms.CharField(max_length=8,required=True, label='Código', 
		help_text='Ingrese una abreviatura. Ej: LO',
		widget=forms.TextInput(attrs={'required': ''}))

	class Meta:
		model = Provincia
		
class CantonForm(ModelForm):
	nombre = forms.CharField(max_length=30,required=True, label='Nombre', 
		help_text='Ingrese el nombre del cantón. Ej: Espíndola',
		widget=forms.TextInput(attrs={'required': ''}))
	abreviatura = forms.CharField(max_length=8,required=True, label='Código', 
		help_text='Ingrese una abreviatura. Ej: ES',
		widget=forms.TextInput(attrs={'required': ''}))
	provincia = forms.ModelChoiceField(required=True, label='Provincia', 
		empty_label='-- Seleccione --' ,queryset=Provincia.objects.all(), help_text='Seleccione la provincia',
		widget=forms.Select(attrs={'required':''}))

	class Meta:
		model = Canton
		
class ParroquiaForm(ModelForm):
	nombre = forms.CharField(max_length=30,required=True, label='Nombre', 
		help_text='Ingrese el nombre de la parroquia. Ej: Amaluza',
		widget=forms.TextInput(attrs={'required': ''}))
	abreviatura = forms.CharField(max_length=8,required=True, label='Código', 
		help_text='Ingrese una abreviatura. Ej: AM',
		widget=forms.TextInput(attrs={'required': ''}))
	canton = forms.ModelChoiceField(required=True, label='Cantón', 
		empty_label='-- Seleccione --' ,queryset=Canton.objects.all(), help_text='Seleccione el cantón',
		widget=forms.Select(attrs={'required':''}))
	class Meta:
		model = Parroquia
		fields = ('nombre','abreviatura','canton')
       
# Forms para dirección
class DireccionForm(ModelForm):
	
    domicilio=forms.CharField(label='Domicilio', max_length=60, required=True,
		help_text='Ingrese la direccion Ej: Sucre 7-19 y Lourdes',
		widget=forms.TextInput(attrs={'required': ''}))
    provincia=forms.ModelChoiceField(queryset=Provincia.objects.all(), empty_label='-- Seleccione --',
    	help_text='Seleccione una provincia Ej: Loja, El Oro',
    	widget=forms.Select(attrs={'required':''}))
    telefono=forms.CharField(max_length=10,label='Teléfono', help_text='Ingrese un tel convencional'+
		' Ej: 072588278',widget=forms.TextInput(attrs={'required': ''}))
		
    queryset_canton = Canton.objects.all()
    queryset_parroquia = Parroquia.objects.all()
    def __init__(self, canton = queryset_canton, parroquia = queryset_parroquia, *args, **kwargs):
    	super(DireccionForm, self).__init__(*args, **kwargs)
    	self.fields['canton']=forms.ModelChoiceField(queryset=canton, empty_label='-- Seleccione --',
    		help_text='Seleccione un canton Ej: Loja - Calvas', 
    		widget=forms.Select(attrs={'required':'', 'disabled':''}))
    	self.fields['parroquia']= forms.ModelChoiceField(queryset=parroquia,
    		empty_label='-- Seleccione --', help_text='Seleccione una parroquia Ej: El Sagrario',
    		widget=forms.Select(attrs={'required':'', 'disabled':''}))
    		
    class Meta:
		model = Direccion



