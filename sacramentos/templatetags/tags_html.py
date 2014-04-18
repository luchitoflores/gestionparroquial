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
	objeto = ParametrizaDiocesis.objects.all()
		
	if objeto[0]:
		return u'<h5>%s</h5><p>%s | %s - Ecuador | Teléfono: %s </p>' % (objeto[0].diocesis, objeto[0].direccion, str(objeto[0].direccion.provincia).title(), objeto[0].direccion.telefono)
	else:
		return ""