# -*- coding:utf-8 -*-
from django import template
from ciudades.forms import DireccionForm
 
register = template.Library()

@register.inclusion_tag('direccion/direccion_form.html', takes_context=True)
def direccion(context):
	form_direccion = DireccionForm()
	ctx = {'form_direccion': form_direccion}
	return ctx