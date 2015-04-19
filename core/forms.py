# -*- coding:utf-8 -*-

__author__ = 'lucho'

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Catalogo, Item, Parametro, Direccion
from .constants import *

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.items_por_catalogo_cod('EST')
        if self.instance.id:
            if self.instance.catalogo.padre:
                self.fields['padre'].queryset = Item.objects.filter(catalogo=self.instance.catalogo.padre)
            else:
                self.fields['padre'].queryset = Item.objects.none()
        else:
            self.fields['padre'].queryset = Item.objects.none()


class CatalogoForm(ModelForm):
    class Meta:
        model = Catalogo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CatalogoForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.items_por_catalogo_cod(COD_CAT_ESTADOS_GENERALES)

        if self.instance.id:
            if self.instance.padre:
                self.fields['padre'].queryset = Catalogo.objects.filter(id=self.instance.padre.id)
            else:
                self.fields['padre'].queryset = Catalogo.objects.all()
        else:
            self.fields['padre'].queryset = Catalogo.objects.all()

class ParametroForm(ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParametroForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = Item.objects.items_por_catalogo_cod('EST')


class SearchLogsForm(forms.Form):
    usuarios = forms.ModelChoiceField(queryset=User.objects.all())
    fecha_inicial = forms.DateField()
    fecha_final = forms.DateField()
    transaccion = forms.ModelChoiceField(queryset=Item.objects.items_por_catalogo_cod(COD_CAT_TRANSACCIONES))

# Forms para dirección
class DireccionForm(ModelForm):
    class Meta:
        model = Direccion
        fields = ('domicilio', 'provincia', 'canton', 'parroquia', 'telefono')
        widgets = {
            'domicilio': forms.TextInput(attrs={'required': ''}),
            'provincia': forms.Select(attrs={'required': ''}),
            'canton': forms.Select(attrs={'required': '', 'disabled': ''}),
            'parroquia': forms.Select(attrs={'required': '', 'disabled': ''}),
        }

    def __init__(self, *args, **kwargs):
        super(DireccionForm, self).__init__(*args, **kwargs)
        self.fields['provincia'].empty_label = '-- Seleccione --'
        self.fields['provincia'].queryset = Item.objects.provincias()
        self.fields['canton'].queryset = Item.objects.none()
        self.fields['canton'].empty_label = '-- Seleccione --'
        self.fields['parroquia'].queryset = Item.objects.none()
        self.fields['parroquia'].empty_label = '-- Seleccione --'