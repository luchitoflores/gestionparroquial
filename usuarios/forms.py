# -*- coding:utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm


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
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'required': ''}),
        }

    def __init__(self, *args, **kwargs):
        super(GruposForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.all()

