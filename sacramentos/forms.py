# -*- coding:utf-8 -*-
from datetime import datetime, date
import time

from django import forms
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.forms.widgets import RadioSelect
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.utils.html import format_html, mark_safe


from .models import (PerfilUsuario, 
					Libro,Sacramento, Matrimonio,Bautismo,Eucaristia,Confirmacion,Bautismo,
					Direccion, Intenciones,NotaMarginal,Parroquia, Iglesia, AsignacionParroquia, PeriodoAsignacionParroquia,
					ParametrizaDiocesis,ParametrizaParroquia, )
from .validators import validate_cedula



class DivErrorList(ErrorList):
	def __unicode__(self):
		return self.as_divs()

	def as_divs(self):
		if not self: 
			return u''
		return u'<div class="error">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


# from django.forms.forms import BoundField

# def add_control_label(f):
#     def control_label_tag(self, contents=None, attrs=None):
#         if attrs is None: 
#         	attrs = {}
#         	attrs['class'] = 'control-label'
#         	return f(self, contents, attrs)
#         	return control_label_tag

# BoundField.label_tag = add_control_label(BoundField.label_tag) 


#Formulario básico para el manejo de usuarios
class UsuarioBaseForm(ModelForm):
	class Meta:
		model = User
		fields= ('first_name', 'last_name', 'email')
		widgets = {
		'first_name': forms.TextInput(attrs={'required': ''}),
		'last_name': forms.TextInput(attrs={'required': ''}),
		}

	def __init__(self, *args, **kwargs):
		# kwargs['error_class'] = DivErrorList
		self.label_suffix = '7777ssss'
		self.error_class = DivErrorList
		# kwargs.setdefault('label_suffix', '####') 
		super(UsuarioBaseForm, self).__init__(*args, **kwargs)	
		self.fields['first_name'].label = 'Nombres *'
		self.fields['first_name'].help_text ='Ingrese los nombres completos. Ej: Juan José'
		self.fields['last_name'].label = 'Apellidos *'
		self.fields['last_name'].help_text ='Ingrese los apellidos completos. Ej: Castro Pardo'
		self.fields['email'].help_text = 'Ingrese correo electrónico. Ej: diocesisloja@gmail.com'
		self.fields['email'].required = False

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if email:
			if self.instance.id:
				usuario = User.objects.filter(email=email).exclude(pk=self.instance.id)
				if usuario:
					raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
			else:
				usuario = User.objects.filter(email=email)
				if usuario:
					raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
		return email

class UsuarioForm(UsuarioBaseForm):
	class Meta(UsuarioBaseForm.Meta):
		fields= UsuarioBaseForm.Meta.fields + ('groups',)
		
	def __init__(self, *args, **kwargs):
		super(UsuarioForm, self).__init__(*args, **kwargs)	
		self.fields['groups'].label = 'Grupos'
		self.fields['groups'].help_text ='Los grupos a los que este usuario pertenece. Un usuario obtendrá todos los permisos concedidos a cada uno sus grupos. Ud. puede seleccionar más de una opción.'
		if self.instance.id:
			self.fields['groups'].required=True
		else: 
			self.fields['groups'].required=False
		
class UsuarioPadreForm(UsuarioBaseForm):
	class Meta(UsuarioBaseForm.Meta):
		pass
		

class UsuarioSecretariaForm(UsuarioBaseForm):
	class Meta(UsuarioBaseForm.Meta):
		pass

	def __init__(self, *args, **kwargs):
		super(UsuarioSecretariaForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['email'].widget = forms.TextInput(attrs={'required': '', 'type':'email'})

class UsuarioSacerdoteForm(UsuarioBaseForm):
	class Meta(UsuarioBaseForm.Meta):
		fields= UsuarioBaseForm.Meta.fields + ('groups',)

	def __init__(self, *args, **kwargs):
		super(UsuarioSacerdoteForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['email'].widget = forms.TextInput(attrs={'required': '', 'type':'email'})
		

class UsuarioAdministradorForm(UsuarioForm):
	class Meta(UsuarioBaseForm.Meta):
		fields= UsuarioBaseForm.Meta.fields + ('groups', 'is_staff')

	def __init__(self, *args, **kwargs):
		super(UsuarioAdministradorForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['email'].widget = forms.TextInput(attrs={'required': '', 'type':'email'})
		self.fields['is_staff'].label = 'Es activo?'
		self.fields['is_staff'].help_text= 'Marque la casilla si quiere que el usuario pueda entrar al sistema'


#Formulario Base para todos los perfiles de usuario
class PersonaBaseForm(ModelForm):
	class Meta:
		model = PerfilUsuario
		fields = ('nacionalidad', 'dni', 'fecha_nacimiento', 'lugar_nacimiento');
		widgets = {
			'nacionalidad': forms.Select(attrs={'required':''}),
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
		}

	def __init__(self, *args, **kwargs):
		super(PersonaBaseForm, self).__init__(*args, **kwargs)
		self.fields['fecha_nacimiento'].label = 'Fecha Nacimiento *'
		self.fields['lugar_nacimiento'].label = 'Lugar Nacimiento *'
		self.fields['nacionalidad'].label = 'Nacionalidad *'


	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	def clean_dni(self):
		cedula = self.cleaned_data.get('dni')
		nacionalidad = self.cleaned_data.get('nacionalidad')

		if cedula:
			if nacionalidad == 'EC':
				if not cedula.isdigit():
					raise forms.ValidationError('El número de cédula no debe contener letras')
					return cedula
				if len(cedula)!=10:
					raise forms.ValidationError('El número de cédula debe ser de 10 dígitos')
					return cedula
				valores = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
				suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
				ultimo_digito = int(str(suma)[-1:])
				if ultimo_digito != 0: 
					if int(cedula[9]) != 10 - ultimo_digito :
						raise forms.ValidationError('El número de cédula no es válido')
						return cedula
				else: 
					if int(cedula[9]) != 0 :
						raise forms.ValidationError('El número de cédula no es válido')
						return cedula

			if self.instance.id:
				usuario = PerfilUsuario.objects.filter(dni=cedula).exclude(pk=self.instance.id)
				if usuario:
					raise forms.ValidationError('Ya existe un usuario registrado con ese número de cédula')
					return cedula
			else:
				usuario = PerfilUsuario.objects.filter(dni=cedula)
				if usuario:
					raise forms.ValidationError('Ya existe un usuario registrado con ese número de cédula')
					return cedula
		
		return cedula



class PerfilUsuarioForm(PersonaBaseForm):
	class Meta(PersonaBaseForm.Meta):
		fields = PersonaBaseForm.Meta.fields + ('sexo', 'estado_civil','profesion', 'padre', 'madre', 'celular');
		# widgets = PersonaBaseForm.Meta.widgets.update({
		# 	'estado_civil':forms.Select(attrs={'required':''})
		# 	})

	def __init__(self, *args, **kwargs):
		super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
		if not self.instance.id:
			self.fields['padre'].queryset=PerfilUsuario.objects.none()
			self.fields['madre'].queryset=PerfilUsuario.objects.none()
		else:
			padre = self.instance.padre
			madre = self.instance.madre
			if padre and madre:
				self.fields['padre'].queryset = PerfilUsuario.objects.filter(pk=padre.id)
				self.fields['madre'].queryset = PerfilUsuario.objects.filter(pk=madre.id)
			elif padre and not madre:
				self.fields['padre'].queryset = PerfilUsuario.objects.filter(pk=padre.id)
				self.fields['madre'].queryset = PerfilUsuario.objects.none()
			elif not padre and madre:
				self.fields['madre'].queryset = PerfilUsuario.objects.filter(pk=madre.id)
				self.fields['padre'].queryset= PerfilUsuario.objects.none()
			else:
				self.fields['padre'].queryset = PerfilUsuario.objects.none()
				self.fields['madre'].queryset = PerfilUsuario.objects.none()


		self.fields['padre'].empty_label='-- Buscar o Crear --'
		self.fields['madre'].empty_label='-- Buscar o Crear --'
		self.fields['sexo'].label = 'Sexo *'
		self.fields['sexo'].widget =  forms.Select(attrs={'required':''}, choices=PerfilUsuario.SEXO_CHOICES)
		self.fields['estado_civil'].label = 'Estado Civil *'
		self.fields['estado_civil'].widget = forms.Select(attrs={'required':''}, choices=PerfilUsuario.ESTADO_CIVIL_CHOICES)

		
class PadreForm(PersonaBaseForm):
	class Meta(PersonaBaseForm.Meta): 
		fields = PersonaBaseForm.Meta.fields + ('estado_civil', 'profesion');
	
	def __init__(self, *args, **kwargs):
		super(PadreForm, self).__init__(*args, **kwargs)
		self.fields['dni'].widget = forms.TextInput(attrs={'required':''})
		self.fields['estado_civil'].label = 'Estado Civil *'
		self.fields['estado_civil'].widget = forms.Select(attrs={'required':''}, choices=PerfilUsuario.ESTADO_CIVIL_CHOICES)
		

class SecretariaForm(PersonaBaseForm):
	class Meta(PersonaBaseForm.Meta):
		fields = PersonaBaseForm.Meta.fields + ('sexo', 'estado_civil')

	def __init__(self, *args, **kwargs):
		super(PadreForm, self).__init__(*args, **kwargs)
		self.fields['dni'].widget = forms.TextInput(attrs={'required':''})
		self.fields['sexo'].widget =  forms.Select(attrs={'required':''}, choices=PerfilUsuario.SEXO_CHOICES)
		self.fields['estado_civil'].label = 'Estado Civil *'
		self.fields['estado_civil'].widget = forms.Select(attrs={'required':''}, choices=PerfilUsuario.ESTADO_CIVIL_CHOICES)

class SacerdoteForm(PersonaBaseForm):
	class Meta(PersonaBaseForm.Meta): 
		fields = PersonaBaseForm.Meta.fields + ('celular',);
	
	def __init__(self, *args, **kwargs):
		super(SacerdoteForm, self).__init__(*args, **kwargs)
		self.fields['dni'].widget = forms.TextInput(attrs={'required':''})

class AdministradorForm(SacerdoteForm):
	class Meta(SacerdoteForm.Meta): 
		fields = SacerdoteForm.Meta.fields + ('sexo',);
	
	def __init__(self, *args, **kwargs):
		super(AdministradorForm, self).__init__(*args, **kwargs)
		self.fields['dni'].widget = forms.TextInput(attrs={'required':''})
		self.fields['sexo'].widget =  forms.Select(attrs={'required':''}, choices=PerfilUsuario.SEXO_CHOICES)


class AdminForm(forms.Form):
	administrador = forms.ModelChoiceField(help_text='Nombre del nuevo administrador', 
		queryset=PerfilUsuario.objects.none(), required=True, empty_label='-- Buscar --',
		widget=forms.Select(attrs={'required':''}))
	is_staff = forms.BooleanField(label='Es activo?', required=False, 
		help_text='Marque la casilla si quiere que el usuario pueda entrar al sistema')


class EmailForm(forms.Form):
	email = forms.EmailField() 


# forms para sacramentos

class LibroForm(ModelForm):	
	class Meta:
		model=Libro
		fields = ('numero_libro', 'tipo_libro', 'fecha_apertura', 'fecha_cierre', 
			'estado', 'primera_pagina', 'primera_acta')
		widgets = {
			'fecha_apertura': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'fecha_cierre': forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date',
				'label':'Fecha Cierre *'}),
			'tipo_libro': forms.Select(attrs={'required':''}),
			'estado': RadioSelect(attrs={'required':''}),
			'numero_libro': forms.TextInput(attrs={'required':''}),
			}

	def clean(self):
		cleaned_data = super(LibroForm, self).clean()
		fecha_apertura=self.cleaned_data.get("fecha_apertura")
		fecha_cierre=self.cleaned_data.get("fecha_cierre")
		if fecha_apertura > date.today():
			msg=u"La fecha de apertura no puede ser mayor a la fecha actual"
			self._errors['fecha_apertura']=self.error_class([msg])
			
		if fecha_cierre:
			if fecha_cierre <= fecha_apertura:
				msg=u"La fecha de cierre no puede ser menor o igual a la fecha de apertura"
				self._errors['fecha_cierre']=self.error_class([msg])
		return cleaned_data
	


class SacramentosForm(ModelForm):
	class Meta:
		model = Sacramento
		fields=('libro','fecha_sacramento', 'celebrante', 
			'lugar_sacramento','padrino','madrina',	'iglesia')
		
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
			'dd/mm/yyyy', 'type':'date'}),
			'lugar_sacramento': forms.TextInput(attrs={'required':''}),
			'iglesia': forms.Select(attrs={'required':''}),
			'celebrante': forms.Select(attrs={'required':''})

			}

	def __init__(self, request, *args, **kwargs):
		super(SacramentosForm, self).__init__(*args, **kwargs)	

		parroquia=request.session.get('parroquia')
		self.fields['celebrante'].empty_label = None
		self.fields['libro'].queryset=Libro.objects.filter(estado='Abierto',tipo_libro='Bautismo', parroquia=parroquia)
		self.fields['libro'].empty_label=None
		self.fields['iglesia'].empty_label= '-- Seleccione --'
		self.fields['iglesia'].queryset = Iglesia.objects.filter(parroquia=parroquia)
		try:
			self.fields['iglesia'].initial=Iglesia.objects.get(principal=True, parroquia=parroquia)
		except ObjectDoesNotExist:
			messages.info(request,'No tiene configurada una Iglesia principal')
			
		if not self.instance.id:
			self.fields['celebrante'].queryset=PerfilUsuario.objects.parroco(parroquia)
		

	def clean(self):
		cleaned_data = super(SacramentosForm, self).clean()
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
				
		if fecha_sacramento > date.today():
			msg=u'La fecha del Sacramento no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		
		return cleaned_data




class BautismoForm(SacramentosForm):
	class Meta(SacramentosForm.Meta):
		model = Bautismo
		fields = SacramentosForm.Meta.fields + ('bautizado', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno',
			'abuela_materna','vecinos_paternos','vecinos_maternos')
	
	def __init__(self, request, *args, **kwargs):
		parroquia=request.session.get('parroquia')
		super(BautismoForm, self).__init__(request, *args, **kwargs)
		self.fields['libro'].queryset = Libro.objects.filter(estado='Abierto',tipo_libro='Bautismo', parroquia=parroquia)
		
		if not self.instance.id:
			self.fields['bautizado']=forms.ModelChoiceField(required=True, queryset=Bautismo.objects.none(),
				 empty_label='-- Buscar o Crear --', label='Feligrés *',
				 help_text='Presione buscar para encontrar un feligres',
				 widget=forms.Select(attrs={'required':''}),
				 error_messages={'invalid': 'El feligrés ya se encuentra bautizado, soy yo'})
		else:
			self.fields['bautizado'].empty_label = None 


	def clean(self):
		cleaned_data = super(BautismoForm, self).clean()
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		persona = self.cleaned_data.get("bautizado")
		fecha_nacimiento = persona.fecha_nacimiento
	
		if fecha_sacramento < fecha_nacimiento:
			msg=u'La fecha del Sacramento no puede ser menor a la fecha de nacimiento del feligres'
			self._errors['fecha_sacramento'] = self.error_class([msg])

		if not self.instance.id:
			if Bautismo.objects.filter(bautizado=persona).exists():
				self._errors['bautizado']=self.error_class(["El feligres ya se encuentra bautizado"])
			elif Eucaristia.objects.filter(feligres=persona) or Confirmacion.objects.filter(confirmado=persona) or Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
				self._errors['bautizado']=self.error_class(["El feligres ya tiene un sacramento posterior al Bautismo"])
		
		return cleaned_data
	      	


class EucaristiaForm(SacramentosForm):
	class Meta(SacramentosForm.Meta):
		model = Eucaristia
		fields = SacramentosForm.Meta.fields + ('feligres',)


	def __init__(self, request, *args, **kwargs):		
		super(EucaristiaForm, self).__init__(request, *args, **kwargs)
		parroquia=request.session.get('parroquia')
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Eucaristia', parroquia=parroquia)

		if not self.instance.id:
			self.fields['feligres']=forms.ModelChoiceField(required=True, queryset=Bautismo.objects.none(),
				 empty_label='-- Buscar o Crear --', label='Feligrés *',
				 help_text='Presione buscar para encontrar un feligres',
				 widget=forms.Select(attrs={'required':''}))
		else:      
			self.fields['feligres'].empty_label = None 
		

	def clean(self):
		cleaned_data = super(EucaristiaForm, self).clean()
		persona = self.cleaned_data.get("feligres")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		fecha_nacimiento=persona.fecha_nacimiento
		
		try:
			fecha_bautismo=Bautismo.objects.get(bautizado=persona).fecha_sacramento
			if fecha_sacramento<fecha_bautismo:
				msg=u'La fecha del Sacramento no puede ser menor a la fecha del Bautismo del feligres'
				self._errors['fecha_sacramento']=self.error_class([msg])
		except ObjectDoesNotExist:
			if fecha_sacramento<fecha_nacimiento:
				msg=u'La fecha del Sacramento no puede ser menor a la fecha de nacimiento del feligres'
				self._errors['fecha_sacramento']=self.error_class([msg])

		if not self.instance.id:
			if Eucaristia.objects.filter(feligres=persona).exists():
				self._errors['feligres']=self.error_class(["El feligres ya realizó la primera comunión"])
			elif Confirmacion.objects.filter(confirmado=persona) or Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
				self._errors['feligres']=self.error_class(["El feligres ya tiene un sacramento posterior a la Primera Comunión"])
				
		return cleaned_data
	
class ConfirmacionForm(SacramentosForm):
	class Meta(SacramentosForm.Meta):
		model = Confirmacion
		fields = SacramentosForm.Meta.fields + ('confirmado', )

	def __init__(self, request, *args, **kwargs):
		super(ConfirmacionForm, self).__init__(request, *args, **kwargs)
		parroquia=request.session.get('parroquia')
		self.fields['libro'].queryset = Libro.objects.filter(estado='Abierto',tipo_libro='Confirmacion',parroquia=parroquia)
		if not self.instance.id:
			self.fields['confirmado']=forms.ModelChoiceField(required=True, queryset=Confirmacion.objects.none(),
				 empty_label='-- Buscar o Crear --', label='Confirmado *',
				 help_text='Presione buscar para encontrar un feligres',
				 widget=forms.Select(attrs={'required':''}))
		else:      
			self.fields['confirmado'].empty_label = None

	def clean(self):
		cleaned_data = super(ConfirmacionForm, self).clean()
		persona = self.cleaned_data.get("confirmado")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		fecha_nacimiento=persona.fecha_nacimiento
		
		if Eucaristia.objects.filter(feligres=persona):
			fecha_eucaristia=Eucaristia.objects.get(feligres=persona).fecha_sacramento
			if fecha_sacramento<fecha_eucaristia:
				msg=u'La fecha del Sacramento no puede ser menor a la fecha de la Primera Comunion del feligres'
				self._errors['fecha_sacramento']=self.error_class([msg])
		elif Bautismo.objects.filter(bautizado=persona):
			fecha_bautismo=Bautismo.objects.get(bautizado=persona).fecha_sacramento
			if fecha_sacramento<fecha_bautismo:
				msg=u'La fecha del Sacramento no puede ser menor a la fecha del Bautismo del feligres'
				self._errors['fecha_sacramento']=self.error_class([msg])
		elif fecha_sacramento<fecha_nacimiento:
				msg=u'La fecha del Sacramento no puede ser menor a la fecha de nacimiento del feligres'
				self._errors['fecha_sacramento']=self.error_class([msg])

		if not self.instance.id:
			if Confirmacion.objects.filter(confirmado=persona).exists():
				self._errors['confirmado']=self.error_class(["El feligres ya realizó la Confirmación"])
			elif Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
				self._errors['confirmado']=self.error_class(["El feligres ya tiene un sacramento posterior a la Confirmación"])
				
		return cleaned_data


class MatrimonioForm(SacramentosForm):
	
	class Meta(SacramentosForm.Meta):
		model=Matrimonio
		fields= SacramentosForm.Meta.fields + ('novio','novia','testigo_novio','testigo_novia',
			'tipo_matrimonio')
		# widgets = {
		# 'tipo_matrimonio': forms.Select(attrs={'required':''}),
		# 'testigo_novio': forms.TextInput(attrs={'required':''}),
		# 'testigo_novia': forms.TextInput(attrs={'required':''}),
		# 'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
		# 'dd/mm/yyyy', 'type':'date'}),
		# 'lugar_sacramento': forms.TextInput(attrs={'required':''}),
		# 'iglesia': forms.TextInput(attrs={'required':''}),
		# 'celebrante': forms.Select(attrs={'required':''})
		# }

	def __init__(self, request, *args, **kwargs):
		super(MatrimonioForm, self).__init__(request, *args, **kwargs)
		parroquia = request.session.get('parroquia')
		self.fields['tipo_matrimonio'].empty_label="-- Seleccione --"
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Matrimonio',parroquia=parroquia)
		self.fields['tipo_matrimonio'].widget = forms.Select(attrs={'required':''}, choices=Matrimonio.TIPO_MATRIMONIO_CHOICES)
		self.fields['testigo_novio'].widget =  forms.TextInput(attrs={'required':''})
		self.fields['testigo_novia'].widget =  forms.TextInput(attrs={'required':''})

		if not self.instance.id:
			self.fields['novio']=forms.ModelChoiceField(required=True, queryset=PerfilUsuario.objects.none(),
				 empty_label='-- Buscar o Crear --', label='Novio *',
				 help_text='Presione buscar para encontrar un feligres',
				 widget=forms.Select(attrs={'required':''}))
			self.fields['novia']=forms.ModelChoiceField(required=True, queryset=PerfilUsuario.objects.none(),
				 empty_label='-- Buscar o Crear --', label='Novia *',
				 help_text='Presione buscar para encontrar un feligres',
				 widget=forms.Select(attrs={'required':''}))
		else:      
			self.fields['novio'].empty_label = None
			self.fields['novia'].empty_label = None

	def clean(self):
		cleaned_data = super(MatrimonioForm, self).clean()
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		novio=self.cleaned_data.get("novio")
		novia=self.cleaned_data.get("novia")

		# Comprobación del novio
		if novio.es_hombre(): 
			if not self.instance.id and novio.es_casado():
				msg=u'El feligrés seleccionado ya está casado'
				self._errors['novio']=self.error_class([msg])
			else:
				fecha_nacimiento_novio=novio.fecha_nacimiento
				if Confirmacion.objects.filter(confirmado=novio):
					fecha_confirmacion=Confirmacion.objects.get(confirmado=novio).fecha_sacramento
					if fecha_sacramento<fecha_confirmacion:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha de la confirmación del novio'
						self._errors['fecha_sacramento']=self.error_class([msg])

				elif Eucaristia.objects.filter(feligres=novio):
					fecha_eucaristia=Eucaristia.objects.get(feligres=novio).fecha_sacramento
					if fecha_sacramento<fecha_eucaristia:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha de la primera comunion del novio'
						self._errors['fecha_sacramento']=self.error_class([msg])

				elif Bautismo.objects.filter(bautizado=novio):
					fecha_bautismo=Bautismo.objects.get(bautizado=novio).fecha_sacramento
					if fecha_sacramento<fecha_bautismo:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha del bautismo del novio'
						self._errors['fecha_sacramento']=self.error_class([msg])
				
				elif fecha_sacramento<fecha_nacimiento_novio:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha de nacimiento del novio'
						self._errors['fecha_sacramento']=self.error_class([msg])
		else:
			msg=u'El feligrés seleccionado no pertenece al género masculino'
			self._errors['novio']=self.error_class([msg])


		# Comprobación de la novia
		if novia.es_mujer():
			if not self.instance.id and novia.es_casado():
					msg=u'La feligrés seleccionada ya está casada'
					self._errors['novia']=self.error_class([msg])
				
			else:
				fecha_nacimiento_novia=novia.fecha_nacimiento
				if Confirmacion.objects.filter(confirmado=novia):
					fecha_confirmacion=Confirmacion.objects.get(confirmado=novia).fecha_sacramento
					if fecha_sacramento<fecha_confirmacion:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha de la confirmación de la novia'
						self._errors['fecha_sacramento']=self.error_class([msg])

				elif Eucaristia.objects.filter(feligres=novia):
					fecha_eucaristia=Eucaristia.objects.get(feligres=novia).fecha_sacramento
					if fecha_sacramento<fecha_eucaristia:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha de la primera comunion de la novia'
						self._errors['fecha_sacramento']=self.error_class([msg])

				elif Bautismo.objects.filter(bautizado=novia):
					fecha_bautismo=Bautismo.objects.get(bautizado=novia).fecha_sacramento
					if fecha_sacramento<fecha_bautismo:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha del bautismo de la novia'
						self._errors['fecha_sacramento']=self.error_class([msg])
				
				elif fecha_sacramento<fecha_nacimiento_novia:
						msg=u'La fecha del Sacramento no puede ser menor a la fecha de nacimiento de la novia'
						self._errors['fecha_sacramento']=self.error_class([msg])
		else: 
			msg=u'La feligrés seleccionada no pertenece al género femenino'
			self._errors['novia']=self.error_class([msg])

		return cleaned_data
	
		

# Forms para Notas Marginales
class NotaMarginalForm(ModelForm):
	class Meta():
		model= NotaMarginal
		fields=('descripcion',)
		widgets = {
		'descripcion': forms.Textarea(attrs={'required':''}),
		}
		
#Forms para Parroquia - Funcionando
class ParroquiaForm(ModelForm):
	class Meta:
		model = Parroquia
		fields = ('nombre',)
		widgets = {
		'nombre': forms.TextInput(attrs={'required':''}),
		}


#Form para asignar parroquia
class AsignarParroquiaForm(ModelForm):
	persona = forms.ModelChoiceField(label = 'Sacerdote', queryset=PerfilUsuario.objects.none(), empty_label='-- Buscar --', widget=forms.Select(attrs={'required':'', 'id':'id_celebrante'})) 
	def __init__(self, parroquia = Parroquia.objects.all(), *args, **kwargs):
		super(AsignarParroquiaForm, self).__init__(*args, **kwargs)
		self.fields['parroquia']=forms.ModelChoiceField(required=True, queryset=parroquia, 
			empty_label=None)

	class Meta:
		model = AsignacionParroquia
		fields = ('persona', 'parroquia')
			
	def clean(self):
		cleaned_data = super(AsignarParroquiaForm, self).clean()
		persona = cleaned_data.get("persona")
		parroquia = cleaned_data.get("parroquia")
		
		try:
			esta_activo= PeriodoAsignacionParroquia.objects.get(asignacion__persona=persona, 
				asignacion__parroquia=parroquia, estado=True)
			if esta_activo:
				print esta_activo
				msg = u"El sacerdote ya tiene un periodo activo en la parroquia elegida"
				self._errors["persona"] = self.error_class([msg])
		except ObjectDoesNotExist:
			esta_activo_otra_parroquia= PeriodoAsignacionParroquia.objects.filter(
				asignacion__persona=persona, estado=True).exclude(asignacion__parroquia=parroquia)
			if esta_activo_otra_parroquia:
				msg = u"El sacerdote ya tiene una asignación activa en otra parroquia"
				self._errors["persona"] = self.error_class([msg])
     
		periodo_activo_otra_parroquia= PeriodoAsignacionParroquia.objects.filter(asignacion__parroquia=parroquia, estado=True).exclude(asignacion__persona=persona)
		if periodo_activo_otra_parroquia:
			msg = u"La parroquia elegida ya tiene asignado un párroco con estado activo"
			self._errors["parroquia"] = self.error_class([msg])
		return cleaned_data

#Form para asignar una secretaria a una parroquia
class AsignarSecretariaForm(ModelForm):
	def clean(self):
		cleaned_data = super(AsignarSecretariaForm, self).clean()
		persona = cleaned_data.get("persona")
		parroquia = cleaned_data.get("parroquia")
		esta_activo_otra_parroquia= PeriodoAsignacionParroquia.objects.filter(asignacion__persona=persona, estado=True).exclude(asignacion__parroquia=parroquia)

		if not persona.user.email:
			mensaje = u"El usuario no tiene correo electrónico. Puede asignarle un correo mediante este "
			msg = mark_safe(u"%s %s" % (mensaje, '<a href="#id_modal_email" data-toggle="modal">formulario</a>'))
			self._errors["persona"] = self.error_class([msg])

		elif esta_activo_otra_parroquia:
			msg = u"La persona elegida ya tiene una asignación activa en otra parroquia"
			self._errors["persona"] = self.error_class([msg])

		return cleaned_data

	def __init__(self, user, persona = PerfilUsuario.objects.none(), estado=False, *args, **kwargs):
		super(AsignarSecretariaForm, self).__init__(*args, **kwargs)
		self.fields['persona']=forms.ModelChoiceField(label = 'Secretario/a *', queryset=persona, empty_label='-- Buscar o Crear --', widget=forms.Select(attrs={'required':''}))
		try:
			parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=user, estado=True).asignacion.parroquia
		except ObjectDoesNotExist:
			raise PermissionDenied

		self.fields['parroquia']=forms.ModelChoiceField(label='Parroquia *', queryset=Parroquia.objects.filter(id=parroquia.id), empty_label=None)

	class Meta:
		model = AsignacionParroquia
		fields = ('persona', 'parroquia')
		


class PeriodoAsignacionParroquiaForm(ModelForm):
	
	def clean(self):
		cleaned_data = super(PeriodoAsignacionParroquiaForm, self).clean()
		inicio = self.cleaned_data.get('inicio')
		fin = self.cleaned_data.get('fin')
		# presente = self.cleaned_data.get('presente')
		# print presente
		estado = self.cleaned_data.get('estado')

		if not self.instance.id and inicio < date.today():
			msg = u"La fecha inicial no puede ser menor a la fecha actual"
			self._errors["inicio"] = self.error_class([msg])
		
		if fin:
			if fin < inicio:
				msg = u"La fecha final no puede ser menor que la fecha inicial"
				self._errors["fin"] = self.error_class([msg])

		return cleaned_data	

	class Meta:
		model = PeriodoAsignacionParroquia
		fields = ('inicio', 'fin', 'estado')
		widgets = {
		'inicio': forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 'type':'date'}),
		'fin': forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'}),
		}

#Form para Intenciones de Misa - Funcionando
class IntencionForm(ModelForm):
	class Meta:
		model = Intenciones
		fields = ('oferente', 'intencion', 'ofrenda', 'fecha', 'hora', 'individual', 'iglesia')
		widgets = {
			'intencion': forms.Textarea(attrs={'required':'', 'title':'intencion'}),
			'oferente': forms.TextInput(attrs={'required':''}),
			'ofrenda': forms.TextInput(attrs={'required':''}),
			'fecha': forms.TextInput(attrs={'required':'', 'type': 'date'}),
			'hora': forms.TextInput(attrs={'required':'', 'type':'time'}),	
			'iglesia': forms.Select(attrs={'required':''}),		
		}

	def __init__(self, *args, **kwargs):
		super(IntencionForm, self).__init__(*args, **kwargs)
		self.fields['iglesia'].empty_label= '-- Seleccione --'
		

	def clean(self):
		cleaned_data= super(IntencionForm,self).clean()
		hora = self.cleaned_data.get('hora')
		fecha = self.cleaned_data.get('fecha')

		if date.today() > fecha:
			msg=u'No puede ingresar fechas en el pasado'
			self._errors['fecha']=self.error_class([msg])

		if hora < datetime.time(datetime.now()) and date.today() == fecha:
	 		msg=u'No se puede ingresar horas en el pasado'
	 		self._errors['hora']=self.error_class([msg])
	  		
		return cleaned_data



class ParametrizaDiocesisForm(ModelForm):
	class Meta:
		model=ParametrizaDiocesis
		fields=('diocesis','obispo')
		widgets={
		'diocesis':forms.TextInput(attrs={'required':''}),
		'obispo':forms.TextInput(attrs={'required':''}),

		}

class ParametrizaParroquiaForm(ModelForm):
	
	class Meta:
		model=ParametrizaParroquia
		fields=('numero_acta','pagina','parroquia')
		widgets={
		'numero_acta':forms.TextInput(attrs={'required':''}),
		'pagina':forms.TextInput(attrs={'required':''}),
		}

	def __init__(self, user, *args, **kwargs):
		super(ParametrizaParroquiaForm, self).__init__(*args, **kwargs)
		
		try:
			parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=user, estado=True).asignacion.parroquia
		except ObjectDoesNotExist:
			raise PermissionDenied

		self.fields['parroquia']=forms.ModelChoiceField(label='Parroquia', 
			queryset=Parroquia.objects.filter(id=parroquia.id),	empty_label=None)

class ReporteIntencionesForm(forms.Form):
   	TIPO_REPORTE = (
		('', '--- Seleccione ---'),
		('d','Diario'),
		('m','Mensual'),
		('a','Anual'),
	)
   	tipo = forms.TypedChoiceField(label=u'Tipo Reporte *', 
		help_text='Seleccione un tipo de reporte Ej: Diario', choices=TIPO_REPORTE, 
		required=True, widget=forms.Select(attrs={'required':''}))

   	fecha=forms.DateField(help_text='Seleccione una fecha ej:18/07/2000',
		required=True,label='Fecha *',
		widget=forms.TextInput(attrs={'required':'','data-date-format': 'dd/mm/yyyy', 
			'type':'date'}))

   	hora=forms.CharField(required=False,help_text='Ingrese una hora ej: 8:00 - 17:00',
    	label='Hora',widget=forms.TextInput(attrs={'type':'time'}))

   

class ReporteSacramentosAnualForm(forms.Form):
	anio=forms.CharField(max_length=4,help_text='Ingrese un año para generar el reporte',label='Año *',
		widget=forms.TextInput(attrs={'required':''}))

class ReportePermisoForm(forms.Form):
	def clean(self):
		cleaned_data=super(ReportePermisoForm,self).clean()
		tipo=cleaned_data.get("tipo")
		feligres=cleaned_data.get("feligres")
		if tipo=='Bautismo':
			f=Bautismo.objects.get(bautizado=feligres)
			if f:
				msg=u'El feligres ya tiene Bautismo'
				self._errors['feligres']=self.error_class([msg])
		if tipo=='Confirmacion':
			f=Confirmacion.objects.get(confirmado=feligres)
			if f:
				msg=u'El feligres ya tiene Confirmacion'
				self._errors['feligres']=self.error_class([msg])
		if tipo=='Primera Comunion':
			f=Eucaristia.objects.get(feligres=feligres)
			if f:
				msg=u'El feligres ya tiene Eucaristia'
				self._errors['feligres']=self.error_class([msg])
		if tipo=='Matrimonio':
			feligres=PerfilUsuario.objects.get(id=feligres)
			if(feligres.sexo=='m'):
				f=Matrimonio.objects.get(novio=feligres,vigente=True)
				if f:
					msg=u'El feligres ya esta casado'
					self._errors['feligres']=self.error_class([msg])
			else:
				f=Matrimonio.objects.get(novia=feligres,vigente=True)
				if f:
					msg=u'La feligres ya esta casada'
					self._errors['feligres']=self.error_class([msg])

		return cleaned_data	

	TIPO_SACRAMENTO = (
		('', '--- Seleccione ---'),
		('Bautismo','Bautismo'),
		('Primera Comunion','Primera Comunion'),
		('Confirmacion','Confirmacion'),
		('Matrimonio','Matrimonio'),
	)
	
   	tipo = forms.TypedChoiceField(label=u'Tipo Sacramento *', 
		help_text='Seleccione un tipo de sacramento', choices=TIPO_SACRAMENTO, 
		required=True, widget=forms.Select(attrs={'required':''}))

   	def __init__(self,feligres = PerfilUsuario.objects.none(), *args, **kwargs):
		super(ReportePermisoForm, self).__init__(*args, **kwargs)
		self.fields['feligres']=forms.ModelChoiceField(label = 'Feligres *', 
			queryset=feligres, empty_label='-- Buscar o Crear --',
			widget=forms.Select(attrs={'required':''}))
		
		
class IglesiaForm(forms.ModelForm):
	class Meta:
		model = Iglesia
		fields = ('nombre', 'principal', 'parroquia')

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(IglesiaForm, self).__init__(*args, **kwargs)
		parroquia = self.request.session.get('parroquia')
		self.fields['parroquia'].queryset = Parroquia.objects.filter(pk=parroquia.pk)
		self.fields['parroquia'].empty_label = None

	def clean_principal(self):
		principal = self.cleaned_data.get('principal')
		parroquia = self.request.session.get('parroquia')
		
		if principal:
			
			if self.instance.id:
				iglesia = Iglesia.objects.filter(principal=True, parroquia=parroquia).exclude(pk=self.instance.id)
				
				if iglesia:
					print iglesia
					raise forms.ValidationError('No pueden existir dos iglesias principales en una parroquia')
			else:
				iglesia = Iglesia.objects.filter(principal=True, parroquia=parroquia)

				if iglesia:
					raise forms.ValidationError('No pueden existir dos iglesias principales en una parroquia')
			
		return principal

