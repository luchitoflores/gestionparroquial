# -*- coding:utf-8 -*-
from django import template
from django.contrib.auth.models import Group, User

from sacramentos.forms import (
	UsuarioPadreForm, PadreForm,PerfilUsuarioForm,
	UsuarioSecretariaForm, SecretariaForm,
	SacerdoteForm, UsuarioSacerdoteForm,
	LibroBaseForm, IglesiaForm, LibroForm,
	NotaMarginalForm,
	)
register = template.Library()

@register.inclusion_tag('includes/feligres_ajax_form.html', takes_context=True)
def feligres(context):
	form_usuario = UsuarioPadreForm()
	form_perfil = PadreForm()
	if context.get('tipo_sacramento'):
		tipo_sacramento = context['tipo_sacramento']
	else:
		tipo_sacramento = None
	ctx = {'form_usuario':form_usuario, 'form_perfil':form_perfil, 'tipo_sacramento':tipo_sacramento}
	return ctx

@register.inclusion_tag('includes/hombre_ajax_form.html', takes_context=True)
def hombre(context):
	form_usuario = UsuarioPadreForm()
	form_perfil = PadreForm()
	if context.get('tipo_sacramento'):
		tipo_sacramento = context['tipo_sacramento']
	else:
		tipo_sacramento = None
	ctx = {'form_usuario':form_usuario, 'form_perfil':form_perfil, 'tipo_sacramento':tipo_sacramento}
	return ctx

@register.inclusion_tag('includes/mujer_ajax_form.html', takes_context=True)
def mujer(context):
	form_usuario = UsuarioPadreForm()
	form_perfil = PadreForm()
	if context.get('tipo_sacramento'):
		tipo_sacramento = context['tipo_sacramento']
	else:
		tipo_sacramento = None
	ctx = {'form_usuario':form_usuario, 'form_perfil':form_perfil, 'tipo_sacramento':tipo_sacramento}
	return ctx

@register.inclusion_tag('includes/secretaria.html', takes_context=True)
def secretaria(context):
	form_perfil = SecretariaForm()
	form_usuario = UsuarioSecretariaForm()
	ctx = {'form_padre':form_perfil,'form_usuariopadre':form_usuario}
	return ctx

@register.inclusion_tag('includes/sacerdote_ajax_form.html', takes_context=True)
def sacerdote(context):
	form_perfil = SacerdoteForm()
	form_usuario = UsuarioSacerdoteForm()
	form_usuario.fields['groups'].initial= Group.objects.filter(name='Sacerdote') 
	ctx = {'form_perfil':form_perfil,'form_usuario':form_usuario}
	return ctx

@register.inclusion_tag('includes/libro_ajax_form.html', takes_context=True)
def libro(context):
	form_libro = LibroBaseForm()
	ctx = {'form_libro': form_libro}
	return ctx

@register.inclusion_tag('includes/iglesia_ajax_form.html', takes_context=True)
def iglesia(context):
	request = context['request']
	form_iglesia = IglesiaForm(request=request)
	ctx = {'form_iglesia': form_iglesia}
	return ctx

@register.inclusion_tag('nota_marginal/nota_marginal.html', takes_context=True)
def nota_marginal(context):
	form_nota=NotaMarginalForm()
	ctx = {'form_nota':form_nota}
	return ctx



