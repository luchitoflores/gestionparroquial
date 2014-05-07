# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
# from .models import Usuario

# class UserCreationForm(forms.ModelForm):
# 	password1 = forms.CharField(label='Clave', widget=forms.PasswordInput)
# 	password2 = forms.CharField(label='Confirme su clave', widget=forms.PasswordInput)

# 	class Meta:
# 		model = Usuario

# 	def clean_password2(self):
# 		password1 = self.cleaned_data.get("password1")
# 		password2 = self.cleaned_data.get("password2")
# 		if password1 and password2 and password1 != password2:
# 			raise forms.ValidationError("Las claves deben ser iguales")
# 		return password2

# 	def save(self, commit=True):
# 		user = super(UserCreationForm, self).save(commit=False)
# 		user.set_password(self.cleaned_data["password1"])
# 		if commit:
# 			user.save()
# 		return user

# class UserChangeForm(forms.ModelForm):
# 	password = ReadOnlyPasswordHashField(help_text= ("Si desea puede cambiar la contraseña aquí: <a href=\"password/\">Cambiar contrseña</a>."))
# 	class Meta:
# 		model = Usuario

# 	def clean_password(self):
# 		return self.initial["password"]

class SendEmailForm(forms.Form):

	def clean_email(self):
		data = self.cleaned_data['email']
		try:
			user = User.objects.get(email=data)
			if not user.is_staff:
				raise forms.ValidationError('Ud no tiene permiso para ingresar al sistema')
				return data
		except ObjectDoesNotExist:
			raise forms.ValidationError('El email ingresado no está asociado a ningún usuario')
			return data

	email = forms.EmailField(help_text='Ingresa tu dirección de correo electrónico ')



class GruposForm(ModelForm):
	class Meta:
		model = Group
		widgets = {
			'name': forms.TextInput(attrs={'required':''}),
			}

	def __init__(self, *args, **kwargs):
		super(GruposForm, self).__init__(*args, **kwargs)
		self.fields['permissions'].queryset= Permission.objects.all()

