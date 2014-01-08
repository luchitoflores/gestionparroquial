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
from django.utils.html import format_html


from .models import (PerfilUsuario, 
					Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,Bautismo,
					Direccion, Intenciones,NotaMarginal,Parroquia,AsignacionParroquia, PeriodoAsignacionParroquia,
					ParametrizaDiocesis,ParametrizaParroquia, )
from .validators import validate_cedula



class DivErrorList(ErrorList):
	def __unicode__(self):
		return self.as_divs()

	def as_divs(self):
		if not self: 
			return u''
		return u'<div class="error">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


#forms para manejo de usuarios
class UsuarioForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *', 
		help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los apellidos completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	groups = forms.ModelMultipleChoiceField(label='Grupos', required=False, queryset= Group.objects.all(),
		help_text = 'Los grupos a los que este usuario pertenece. Un usuario obtendrá'+
		' todos los permisos concedidos a cada uno sus grupos. Ud. puede seleccionar más de una opción.',
		 widget=forms.CheckboxSelectMultiple())
	email = forms.EmailField(label='Email', 
		help_text='Ingrese correo electrónico. Ej: diocesisloja@gmail.com', required=False)
	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email', 'groups')
		
	def __init__(self, *args, **kwargs):
		super(UsuarioForm, self).__init__(*args, **kwargs)

		if self.instance.id:
			self.fields['groups'].required=True
		else: 
			self.fields['groups'].required=False

	def email_clean(self):
		email = self.cleaned_data.get('email')
		if email:
			if self.instance.id:
				usuario = PerfilUsuario.objects.filter(user__email=email).exclude(pk=self.instance.id)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
			else:
				usuario = PerfilUsuario.objects.filter(user__email=email)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
		return email


class UsuarioPadreForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *',
	 help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los apellidos completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	email = forms.EmailField(required=False, label='Email', 
		help_text='Ingrese su dirección de correo electrónico')

	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email')

	def email_clean(self):
		email = self.cleaned_data.get('email')
		if email:
			if self.instance.id:
				usuario = PerfilUsuario.objects.filter(user__email=email).exclude(pk=self.instance.id)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
			else:
				usuario = PerfilUsuario.objects.filter(user__email=email)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
		return email

class UsuarioSecretariaForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *',
	 help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	email = forms.EmailField(required=True, label='Email *', 
		help_text='Ingrese su dirección de correo electrónico',
		widget=forms.TextInput(attrs={'required': ''}))

	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email')


	def email_clean(self):
		email = self.cleaned_data.get('email')
		if email:
			if self.instance.id:
				usuario = PerfilUsuario.objects.filter(user__email=email).exclude(pk=self.instance.id)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
			else:
				usuario = PerfilUsuario.objects.filter(user__email=email)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
		return email

class UsuarioSacerdoteForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *', 
		help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	groups = forms.ModelMultipleChoiceField(label='Grupos *', queryset= Group.objects.all().exclude(name='Feligres'),
		help_text = 'Los grupos a los que este usuario pertenece. '+
		'Un usuario obtendrá todos los permisos concedidos a cada uno sus grupos.'+
		' Ud. puede seleccionar más de una opción.', widget=forms.CheckboxSelectMultiple(), required=False)
	email = forms.EmailField(required=True, label='Email *', 
		help_text='Ingrese el email. Ej: juan_salinas12@gmail.com',
		widget=forms.TextInput(attrs={'required': ''}))
	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email','groups')

	def __init__(self, *args, **kwargs):
		super(UsuarioSacerdoteForm, self).__init__(*args, **kwargs)
		if self.instance.id:
			self.fields['groups'].required=True
		else: 
			self.fields['groups'].required=False

	def email_clean(self):
		email = self.cleaned_data.get('email')
		if email:
			if self.instance.id:
				usuario = PerfilUsuario.objects.filter(user__email=email).exclude(pk=self.instance.id)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
			else:
				usuario = PerfilUsuario.objects.filter(user__email=email)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
		return email

class UsuarioAdministradorForm(ModelForm):
	first_name = forms.CharField(required=True, label='Nombres *', 
		help_text='Ingrese los nombres completos. Ej: Juan José',
		widget=forms.TextInput(attrs={'required': ''}))
	last_name = forms.CharField(required=True, label='Apellidos *', 
		help_text='Ingrese los nombres completos. Ej: Castro Pardo',
		widget=forms.TextInput(attrs={'required': ''}))
	groups = forms.ModelMultipleChoiceField(required=False, label='Grupos *', queryset= Group.objects.all().order_by('name'),
		help_text = 'Los grupos a los que este usuario pertenece. '+
		'Un usuario obtendrá todos los permisos concedidos a cada uno sus grupos.'+
		' Ud. puede seleccionar más de una opción.', widget=forms.CheckboxSelectMultiple())
	email = forms.EmailField(required=True, label='Email *', 
		help_text='Ingrese el email. Ej: juan_salinas12@gmail.com',
		widget=forms.TextInput(attrs={'required': ''}))
	is_staff = forms.BooleanField(label='Es activo?', required=False,
		help_text='Marque la casilla si quiere que el usuario pueda entrar al sistema')
	
	class Meta():
		model = User
		fields= ('first_name', 'last_name', 'email','groups', 'is_staff')

	def __init__(self, *args, **kwargs):
		super(UsuarioAdministradorForm, self).__init__(*args, **kwargs)
		
		if self.instance.id:
			self.fields['groups'].required=True
		else: 
			self.fields['groups'].required=False

	def email_clean(self):
		email = self.cleaned_data.get('email')
		if email:
			if self.instance.id:
				usuario = PerfilUsuario.objects.filter(user__email=email).exclude(pk=self.instance.id)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
			else:
				usuario = PerfilUsuario.objects.filter(user__email=email)
				raise forms.ValidationError('Ya existe un usuario registrado con ese correo electrónico')
		return email


		

class PerfilUsuarioForm(ModelForm):

	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	def clean_dni(self):
		cedula = self.cleaned_data['dni']
		nacionalidad = self.cleaned_data['nacionalidad']

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

	
	def __init__(self, padre = PerfilUsuario.objects.none() , madre = PerfilUsuario.objects.none(), *args, **kwargs):
		super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
		self.fields['padre']=forms.ModelChoiceField(required=False, queryset=padre, 
			empty_label='-- Buscar o Crear --')
		self.fields['madre']=forms.ModelChoiceField(required=False, queryset=madre, 
			empty_label='-- Buscar o Crear --')
		self.fields['sexo'].label = 'Sexo *'
		self.fields['nacionalidad'].label = 'Nacionalidad *'
		self.fields['estado_civil'].label = 'Estado Civil *'
		self.fields['fecha_nacimiento'].label = 'Fecha Nacimiento *'
		self.fields['lugar_nacimiento'].label = 'Lugar Nacimiento *'

	class Meta():
		model = PerfilUsuario
		fields = ('nacionalidad', 'dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil' ,
			'profesion', 'padre', 'madre', 'celular');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			'nacionalidad': forms.Select(attrs={'required':''}),
			'sexo': forms.Select(attrs={'required':''}),
			'estado_civil': forms.Select(attrs={'required':''}),
			}
		
class PadreForm(ModelForm):
	def clean_dni(self):
		cedula = self.cleaned_data['dni']
		nacionalidad = self.cleaned_data['nacionalidad']

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

	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data
	
	lugar_nacimiento = forms.CharField(help_text='Ingrese el lugar de  nacimiento ej: Loja ', 
		required=True,label='Lugar de Nacimiento',
		widget=forms.TextInput(attrs={'required':''}))
	class Meta(): 
		model = PerfilUsuario
		fields = ('nacionalidad','dni', 'fecha_nacimiento', 'lugar_nacimiento', 'estado_civil',
		 'profesion');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'dni': forms.TextInput(attrs={'required':''}),
			'nacionalidad': forms.Select(attrs={'required':''}),
			'estado_civil': forms.Select(attrs={'required':''}),
			
			}



class SecretariaForm(ModelForm):
	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	def clean_dni(self):
		cedula = self.cleaned_data['dni']
		nacionalidad = self.cleaned_data['nacionalidad']

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

	class Meta():
		model = PerfilUsuario
		fields = ('nacionalidad', 'dni', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo', 'estado_civil');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			'dni': forms.TextInput(attrs={'required':''}),
			'nacionalidad': forms.Select(attrs={'required':''}),
			'sexo': forms.Select(attrs={'required':''}),
			'estado_civil': forms.Select(attrs={'required':''}),
			}


class SacerdoteForm(ModelForm):
	def clean_fecha_nacimiento(self):
		data = self.cleaned_data['fecha_nacimiento']
		if data > date.today():
			raise forms.ValidationError('La fecha de nacimiento no puede ser mayor a la fecha actual')
		return data

	def clean_dni(self):
		cedula = self.cleaned_data['dni']
		nacionalidad = self.cleaned_data['nacionalidad']

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

	class Meta(): 
		model = PerfilUsuario
		fields = ('nacionalidad','dni', 'fecha_nacimiento', 'lugar_nacimiento', 'celular');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			'dni': forms.TextInput(attrs={'required':''}),
			'nacionalidad': forms.Select(attrs={'required':''}),
			}


class AdministradorForm(SacerdoteForm):
	class Meta(SacerdoteForm.Meta): 
		fields = ('nacionalidad','dni', 'fecha_nacimiento', 'lugar_nacimiento', 'celular', 'sexo');
		widgets = {
			'fecha_nacimiento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'lugar_nacimiento': forms.TextInput(attrs={'required':''}),
			'dni': forms.TextInput(attrs={'required':''}),
			'nacionalidad': forms.Select(attrs={'required':''}),
			'sexo': forms.Select(attrs={'required':''}),
			}

class AdminForm(forms.Form):
	administrador = forms.ModelChoiceField(help_text='Nombre del nuevo administrador', 
		queryset=PerfilUsuario.objects.none(), required=True, empty_label='-- Buscar --',
		widget=forms.Select(attrs={'required':''}))
	is_staff = forms.BooleanField(label='Es activo?', required=False, 
		help_text='Marque la casilla si quiere que el usuario pueda entrar al sistema')

	# def __init__(self, *args, **kwargs):
	# 	super(AdminForm, self).__init__(self, *args, **kwargs):

class EmailForm(forms.Form):
	email = forms.EmailField() 


# forms para sacramentos

class LibroForm(ModelForm):
	

	def clean(self):
		cleaned_data = super(LibroForm, self).clean()
		# numero = self.cleaned_data.get("numero_libro")
		# tipo = self.cleaned_data.get("tipo_libro")
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
	

	TIPO_LIBRO_CHOICES = (
		('', '--- Seleccione ---'),
		('Bautismo','Bautismo'),
        ('Eucaristia','Primera Comunión'), 
        ('Confirmacion','Confirmación'),
        ('Matrimonio','Matrimonio'),
                 
    )

	ESTADO_CHOICES=(
		('Abierto','Abierto'),
		('Cerrado','Cerrado'),
		)
	numero_libro=forms.IntegerField(required=True, label='Numero Libro *', 
		widget=forms.TextInput(attrs={'required': ''}),
		help_text='Ingrese un numero para libro ej:1 - 35')

	tipo_libro= forms.TypedChoiceField(label=u'Tipo de Libro *', choices=TIPO_LIBRO_CHOICES, 
		required=True, widget=forms.Select(attrs={'required':''}),
		help_text='Seleccione un tipo de libro Ej: Bautismo')

	estado=forms.ChoiceField(required=True,choices=ESTADO_CHOICES,label='Estado *', 
		widget=RadioSelect(attrs={'required':''}))
	# fecha_apertura = forms.CharField(label=u'Fecha de Apertura', initial=date.today(),
	# 	widget=forms.TextInput(attrs={'required':'', 'data-date-format': 'dd/mm/yyyy', 
	# 		'type':'date'}),help_text='Seleccione una fecha ej:17/12/2010')
	# fecha_cierre = forms.CharField(required=False,label=u'Fecha de Cierre', 
	# 	widget=forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date'
	# 		}),help_text='Seleccione una fecha ej:17/12/2010')
	
	
	class Meta():
		model=Libro
		fields = ('numero_libro', 'tipo_libro', 'fecha_apertura', 'fecha_cierre', 
			'estado')
		widgets = {
			'fecha_apertura': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			'fecha_cierre': forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type':'date',
				'label':'Fecha Cierre *'}),
			
			}


class BautismoForm(ModelForm):
	

	def clean(self):
		cleaned_data = super(BautismoForm, self).clean()
		libro = self.cleaned_data.get("libro")
		persona = self.cleaned_data.get("bautizado")
		print "persona: %s " % type(persona)
		print "Feligres: %s " % (persona)
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		if fecha_sacramento>date.today():
			msg=u'La fecha del Bautismo no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		
		if Eucaristia.objects.filter(feligres=persona) or Confirmacion.objects.filter(confirmado=persona) or Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
			self._errors['bautizado']=self.error_class(["El feligres ya tiene un sacramento posterior al Bautismo"])
		
		# if persona.es_comunion or persona.es_confirmado or persona.es_novio or persona.es_novia:
		# 	print "Comunion: %s"%persona.es_comunion
		# 	print "Confirmación: %s"%persona.es_confirmado
		# 	print "Novio: %s"%persona.es_novio
		# 	print "Novia: %s"%persona.es_novia
		# 	self._errors['bautizado']=self.error_class(["El feligres ya tiene un sacramento posterior al Bautismo"])
		return cleaned_data

	lugar_sacramento = forms.CharField(help_text='Ingrese el lugar del sacramento ej: Loja ', 
		required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(help_text='Ingrese el nombre de la iglesia: San Jose',
		required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}))
	libro=forms.ModelChoiceField(help_text='Seleccione un libro para el Bautismo',
		queryset=Libro.objects.none(),empty_label=None)

	def __init__(self,user, bautizado=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
		*args, **kwargs):

		super(BautismoForm, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Bautismo',parroquia=asignacion.parroquia)
		self.fields['bautizado']=forms.ModelChoiceField(required=True, queryset=bautizado,
			 empty_label='-- Buscar o Crear --',label='Feligrés *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Buscar o Crear--',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			widget=forms.Select(attrs={'required':''}))
		self.fields['vecinos_paternos'].label='Residencia Abuelos Paternos'
		self.fields['vecinos_maternos'].label='Residencia Abuelos Maternos'

		

		      	
	class Meta():
		model=Bautismo
		fields=('bautizado','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno',
			'abuela_materna','vecinos_paternos','vecinos_maternos')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}

class BautismoFormEditar(ModelForm):
	def clean(self):
		cleaned_data = super(BautismoFormEditar, self).clean()
		libro = self.cleaned_data.get("libro")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		persona = self.cleaned_data.get("bautizado")
		if fecha_sacramento>date.today():
			msg=u'La fecha del Bautismo no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		# if persona.es_casado:
		# 	self._errors['bautizado']=self.error_class(["El feligres seleccionado ya está casado"])
		# if Eucaristia.objects.filter(feligres=persona) or Confirmacion.objects.filter(confirmado=persona) or Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
		# 	self._errors['bautizado']=self.error_class(["El feligres ya tiene un sacramento posterior al Bautismo"])
		# if persona.es_comunion or persona.es_confirmado or persona.es_novio or persona.es_novia:
		# 	self._errors['bautizado']=self.error_class(["El feligres ya tiene un sacramento posterior al Bautismo"])
		return cleaned_data
	
	lugar_sacramento = forms.CharField(help_text='Ingrese el lugar del sacramento ej: Loja ', 
		required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}))
	iglesia = forms.CharField(help_text='Ingrese el nombre de la iglesia: San Jose',
		required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}))
	libro=forms.ModelChoiceField(empty_label=None,queryset=Libro.objects.none(),
		help_text='Seleccione un libro para el Bautismo')


	def __init__(self,user,bautizado=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
	 *args, **kwargs):

		super(BautismoFormEditar, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Bautismo',parroquia=asignacion.parroquia)
		self.fields['bautizado']=forms.ModelChoiceField(required=True, queryset=bautizado,
			 empty_label=None,label='Feligrés *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['vecinos_paternos'].label='Residencia Abuelos Paternos'
		self.fields['vecinos_maternos'].label='Residencia Abuelos Maternos'
			 

      
	
	class Meta():
		model=Bautismo
		fields=('bautizado','libro','celebrante','fecha_sacramento',
			'lugar_sacramento','padrino','madrina',
			'iglesia', 'abuelo_paterno', 'abuela_paterna', 'abuelo_materno',
			'abuela_materna','vecinos_paternos','vecinos_maternos')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class EucaristiaForm(ModelForm):
	# def clean_fecha_sacramento(self):
	# 	data = self.cleaned_data['fecha_sacramento']
	# 	if data > date.today():
	# 		raise forms.ValidationError('La fecha de la Eucaristia no puede ser mayor a la fecha actual')
	# 	return data
	def clean(self):
		cleaned_data = super(EucaristiaForm, self).clean()
		libro = self.cleaned_data.get("libro")
		numero = self.cleaned_data.get("numero_acta")
		pagina=self.cleaned_data.get("pagina")
		persona = self.cleaned_data.get("feligres")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		print persona

		if fecha_sacramento>date.today():
			msg=u'La fecha de la Eucaristia no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		
		# if persona.es_casado:
		# 	self._errors['feligres']=self.error_class(["El feligres seleccionado ya está casado"])
		if Confirmacion.objects.filter(confirmado=persona) or Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
			self._errors['feligres']=self.error_class(["El feligres ya tiene un sacramento posterior a la Primera Comunión"])
		# if persona.es_confirmado or persona.es_novio or persona.es_novia:
		# 	self._errors['feligres']=self.error_class(["El feligres ya tiene un sacramento posterior a la Primera Comunión"])
		
		return cleaned_data
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Eucaristia')

	def __init__(self,user, feligres=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
		*args, **kwargs):
		
		super(EucaristiaForm, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Eucaristia',parroquia=asignacion.parroquia)
		self.fields['feligres']=forms.ModelChoiceField(required=True, queryset=feligres,
			 empty_label='-- Buscar --',label='Feligrés *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Buscar --',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Eucaristia
		fields=('feligres','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}


class EucaristiaFormEditar(ModelForm):
	def clean(self):
		cleaned_data = super(EucaristiaFormEditar, self).clean()
		libro = self.cleaned_data.get("libro")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		persona = self.cleaned_data.get("feligres")
		if fecha_sacramento>date.today():
			msg=u'La fecha de la Eucaristia no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		# if persona.es_casado:
		# 	self._errors['feligres']=self.error_class(["El feligres seleccionado ya está casado"])
		# if Confirmacion.objects.filter(confirmado=persona) or Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
		# 	self._errors['feligres']=self.error_class(["El feligres ya tiene un sacramento posterior a la Primera Comunión"])
		# if persona.es_confirmado or persona.es_novio or persona.es_novia:
		# 	self._errors['feligres']=self.error_class(["El feligres ya tiene un sacramento posterior a la Primera Comunion"])
		return cleaned_data

	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	# celebrante = forms.ModelChoiceField(help_text='Seleccione un celebrante',
	# 	queryset=PerfilUsuario.objects.filter(profesion='Sacerdote'),
	# 	empty_label='-- Seleccione --')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Eucaristia')

	def __init__(self,user,feligres=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
	 *args, **kwargs):
		
		super(EucaristiaFormEditar, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		# asignacion = AsignacionParroquia.objects.get(persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Eucaristia',parroquia=asignacion.parroquia)
		self.fields['feligres']=forms.ModelChoiceField(required=True, queryset=feligres,
			 empty_label=None,label='Feligrés *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Eucaristia
		fields=('feligres','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','celebrante','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class ConfirmacionForm(ModelForm):

	def clean(self):
		cleaned_data = super(ConfirmacionForm, self).clean()
		libro = self.cleaned_data.get("libro")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		persona = self.cleaned_data.get("confirmado")
		
		if fecha_sacramento>date.today():
			msg=u'La fecha de Confirmacion no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		
		# if persona.es_casado:
		# 	self._errors['confirmado']=self.error_class(["El feligres seleccionado ya está casado"])
		if Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
			self._errors['confirmado']=self.error_class(["El feligres ya tiene un sacramento posterior a la Confirmación"])
		# if persona.es_novio or persona.es_novia:
		# 	self._errors['confirmado']=self.error_class(["El feligres ya tiene un sacramento posterior a la Confirmación"])
		
		return cleaned_data
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Confirmacion')

	def __init__(self,user, confirmado=PerfilUsuario.objects.none(),celebrante=PerfilUsuario.objects.none(),
		*args, **kwargs):
		
		super(ConfirmacionForm, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Confirmacion',parroquia=asignacion.parroquia)
		self.fields['confirmado']=forms.ModelChoiceField(required=True, queryset=confirmado,
			 empty_label='-- Buscar --',label='Feligrés *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Buscar --',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))



	class Meta():
		model=Confirmacion
		fields=('confirmado','celebrante','libro','fecha_sacramento',
			'lugar_sacramento','padrino','madrina','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}

class ConfirmacionFormEditar(ModelForm):
	def clean(self):
		cleaned_data = super(ConfirmacionFormEditar, self).clean()
		libro = self.cleaned_data.get("libro")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		persona = self.cleaned_data.get("confirmado")

		if fecha_sacramento>date.today():
			msg=u'La fecha de Confirmacion no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])

		# if persona.es_casado:
		# 	self._errors['bautizado']=self.error_class(["El feligres seleccionado ya está casado"])
		# if Matrimonio.objects.filter(novio=persona) or Matrimonio.objects.filter(novia=persona):
		# 	self._errors['confirmado']=self.error_class(["El feligres ya tiene un sacramento posterior a la Confirmación"])
		# if persona.es_novio or persona.es_novia:
		# 	self._errors['bautizado']=self.error_class(["El feligres ya tiene un sacramento posterior a la Confirmación"])
		return cleaned_data
	
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),
		help_text='Seleccione un libro para la Confirmacion')

	def __init__(self,user, confirmado=PerfilUsuario.objects.none(),
		celebrante=PerfilUsuario.objects.none(),*args, **kwargs):
		
		super(ConfirmacionFormEditar, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		# asignacion = AsignacionParroquia.objects.get(persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Confirmacion',parroquia=asignacion.parroquia)
		self.fields['confirmado']=forms.ModelChoiceField(required=True, queryset=confirmado,
			 empty_label=None,label='Feligrés *',
			 help_text='Presione buscar para encontrar un feligres',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Confirmacion
		fields=('confirmado','libro','fecha_sacramento',
			'lugar_sacramento','celebrante','padrino','madrina','iglesia')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}



class MatrimonioForm(ModelForm):
	def clean(self):
		cleaned_data = super(MatrimonioForm, self).clean()
		libro = self.cleaned_data.get("libro")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		if fecha_sacramento>date.today():
			msg=u'La fecha del Matrimonio no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		
		return cleaned_data
	
	TIPO_MATRIMONIO_CHOICES=(
		('', '--- Seleccione ---'),
        ('Catolico','Catolico'),
        ('Mixto','Mixto'),
        )
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	tipo_matrimonio = forms.TypedChoiceField(label=u'Tipo Matrimonio *', 
		help_text='Elija tipo de matrimonio Ej: Catolico o Mixto', 
		choices=TIPO_MATRIMONIO_CHOICES, required=True, 
		widget=forms.Select(attrs={'required':''}))

	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	testigo_novio= forms.CharField(required=True,label='Testigo *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testigo ej: Pablo Robles')
	testigo_novia= forms.CharField(required=True,label='Testiga *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testiga ej:Maria Pincay')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),help_text='Seleccione un libro para el Matrimonio')


	def __init__(self,user,novio=PerfilUsuario.objects.none(),novia=PerfilUsuario.objects.none(),
	celebrante=PerfilUsuario.objects.none(), *args, **kwargs):
		
		super(MatrimonioForm, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		# asignacion = AsignacionParroquia.objects.get(persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			estado='Abierto',tipo_libro='Matrimonio',parroquia=asignacion.parroquia)
		self.fields['novio']=forms.ModelChoiceField(required=True, queryset=novio, 
			empty_label='-- Buscar --',label='Novio *',
			 help_text='Presione buscar para encontrar un novio',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['novia']=forms.ModelChoiceField(required=True, queryset=novia, 
			empty_label='-- Buscar --',label='Novia *',
			 help_text='Presione buscar para encontrar una novia',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante'] = forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label='-- Buscar --',label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))

	class Meta():
		model=Matrimonio
		fields=('libro','fecha_sacramento','lugar_sacramento','celebrante',
			'padrino','madrina','iglesia','novio','novia','testigo_novio','testigo_novia',
			'tipo_matrimonio')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}


class MatrimonioFormEditar(ModelForm):
	def clean(self):
		cleaned_data = super(MatrimonioFormEditar, self).clean()
		libro = self.cleaned_data.get("libro")
		fecha_sacramento=self.cleaned_data.get("fecha_sacramento")
		if fecha_sacramento>date.today():
			msg=u'La fecha del Matrimonio no debe ser mayor a la fecha actual'
			self._errors['fecha_sacramento']=self.error_class([msg])
		return cleaned_data


	TIPO_MATRIMONIO_CHOICES=(
		('', '--- Seleccione ---'),
        ('Catolico','Catolico'),
        ('Mixto','Mixto'),
        )
	tipo_matrimonio = forms.TypedChoiceField(label=u'Tipo Matrimonio *', 
		help_text='Elija tipo de matrimonio Ej: Catolico o Mixto', 
		choices=TIPO_MATRIMONIO_CHOICES, required=True, 
		widget=forms.Select(attrs={'required':''}))
	lugar_sacramento = forms.CharField(required=True,label='Lugar del Sacramento *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el lugar del sacramento ej: Loja ')
	iglesia = forms.CharField(required=True,label='Iglesia *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la iglesia: San Jose')
	testigo_novio= forms.CharField(required=True,label='Testigo *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testigo ej: Pablo Robles')
	testigo_novia= forms.CharField(required=True,label='Testiga *',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de testiga ej:Maria Pincay')
	libro=forms.ModelChoiceField(empty_label=None,label='Libro',
		queryset=Libro.objects.none(),help_text='Seleccione un libro para el Matrimonio')

	def __init__(self,user,novio=PerfilUsuario.objects.none(),novia=PerfilUsuario.objects.none(), 
		celebrante=PerfilUsuario.objects.none(),*args, **kwargs):
		
		super(MatrimonioFormEditar, self).__init__(*args, **kwargs)
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=user,
				periodoasignacionparroquia__estado=True)
		except ObjectDoesNotExist:
			raise PermissionDenied
		# asignacion = AsignacionParroquia.objects.get(persona__user=user)
		self.fields['libro'].queryset = Libro.objects.filter(
			tipo_libro='Matrimonio',parroquia=asignacion.parroquia)
		self.fields['novio']=forms.ModelChoiceField(required=False, queryset=novio, 
			empty_label=None,label='Novio *',
			 help_text='Presione buscar para encontrar un novio',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['novia']=forms.ModelChoiceField(required=False, queryset=novia, 
			empty_label=None,label='Novia *',
			 help_text='Presione buscar para encontrar una novia',
			 widget=forms.Select(attrs={'required':''}))
		self.fields['celebrante']=forms.ModelChoiceField(required=True,queryset=celebrante,
			empty_label=None,label='Celebrante *',
			 help_text='Presione buscar para encontrar un sacerdote',
			 widget=forms.Select(attrs={'required':''}))


	class Meta():
		model=Matrimonio
		fields=('libro','fecha_sacramento','lugar_sacramento','celebrante',
			'padrino','madrina','iglesia','novio','novia','testigo_novio','testigo_novia',
			'tipo_matrimonio')
		widgets = {
			'fecha_sacramento': forms.TextInput(attrs={'required':'', 'data-date-format': 
				'dd/mm/yyyy', 'type':'date'}),
			
			}


# Forms para Notas Marginales
class NotaMarginalForm(ModelForm):
	
	descripcion=forms.CharField(required=True,label='Descripción *',
		widget=forms.Textarea(attrs={'required':''}),
		help_text='Ingrese una descripcion ej: di copia para matrimonio')
	class Meta():
		model= NotaMarginal
		fields=('descripcion',)
		


#Forms para Parroquia - Funcionando
class ParroquiaForm(ModelForm):
	nombre=forms.CharField(required=True,label='Nombre de parroquia',
		widget=forms.TextInput(attrs={'required':''}),
		help_text='Ingrese el nombre de la parroquia Ej: El Cisne')
	class Meta:
		model = Parroquia
		fields = ('nombre',)

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
		if esta_activo_otra_parroquia:
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

		if inicio < date.today():
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

class PeriodoAsignacionParroquiaUpdateForm(ModelForm):
	
	def clean(self):
		cleaned_data = super(PeriodoAsignacionParroquiaUpdateForm, self).clean()
		inicio = self.cleaned_data.get('inicio')
		fin = self.cleaned_data.get('fin')
		# presente = self.cleaned_data.get('presente')
		estado = self.cleaned_data.get('estado')
		# print presente

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
	# fecha = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
	#  widget=forms.DateTimeInput(attrs={'type':'datetime-local'}),
	#  help_text='Ingrese la fecha de la intencion ej:2010-11-13')

	
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


	# def clean_fecha(self):
	# 	data = self.cleaned_data['fecha']
	# 	if date.today() > data:
	#   		raise forms.ValidationError('Lo siento, no puede usar fechas en el pasado')
	#  	return data
	
	# def clean_hora(self):
	#  	data = self.cleaned_data['hora']
	#  	data_fecha = self.cleaned_data['fecha']
	#  	print data
	#  	# print datetime.time() 
	#   	if data < datetime.time(datetime.now()) and date.today() > data_fecha:
	#  		raise forms.ValidationError('Lo siento, no puede usar fechas en el pasado')
	#  	return data




	class Meta:
		model = Intenciones
		fields = ('oferente', 'intencion', 'ofrenda', 'fecha', 'hora', 'individual', 'iglesia')
		widgets = {
			'intencion': forms.Textarea(attrs={'required':'', 'title':'intencion'}),
			'oferente': forms.TextInput(attrs={'required':''}),
			'ofrenda': forms.TextInput(attrs={'required':'',  'pattern':'[0-9]+'}),
			'fecha': forms.TextInput(attrs={'required':'', 'type': 'date'}),
			'hora': forms.TextInput(attrs={'required':'', 'type':'time'}),	
			'iglesia': forms.TextInput(attrs={'required':''}),		
		}

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
	anio=forms.CharField(help_text='Ingrese un año para generar el reporte',label='Año *',
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
		if tipo=='Eucaristia':
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
		('Eucaristia','Eucaristia'),
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
		
		
