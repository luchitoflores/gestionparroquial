# -*- coding:utf-8 -*-
from django import template
from sacramentos.forms import UsuarioForm, PadreForm,PerfilUsuarioForm
from sacramentos.models import ParametrizaDiocesis
register = template.Library()

@register.filter(is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})

@register.simple_tag
def footer_tag():
	objetos = ParametrizaDiocesis.objects.all()
	objeto = ''
	for o in objetos:
		objeto = o
	if objeto:
		return u'<h5>%s</h5><p>%s | %s - Ecuador | Teléfono: %s </p>' % (objeto.diocesis, objeto.direccion, str(objeto.direccion.provincia).title(), objeto.direccion.telefono)
	else:
		return ""