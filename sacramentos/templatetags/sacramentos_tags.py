# -*- coding:utf-8 -*-
from django import template
from sacramentos.forms import (
	UsuarioPadreForm, PadreForm,PerfilUsuarioForm,
	NotaMarginalForm, UsuarioSecretariaForm, SecretariaForm,
	LibroForm, IglesiaForm
	)
register = template.Library()

@register.inclusion_tag('usuario/feligres.html', takes_context=True)
def feligres(context):
	form_usuario = UsuarioPadreForm()
	form_perfil = PadreForm()
	ctx = {'form_usuariopadre':form_usuario, 'form_padre':form_perfil}
	return ctx

@register.inclusion_tag('usuario/secretaria.html', takes_context=True)
def secretaria(context):
	form_perfil = SecretariaForm()
	form_usuario = UsuarioSecretariaForm()
	ctx = {'form_padre':form_perfil,'form_usuariopadre':form_usuario}
	return ctx

@register.inclusion_tag('includes/libro_ajax_form.html', takes_context=True)
def libro_ajax(context):
	form_libro = LibroForm()
	ctx = {'form_libro': form_libro}
	return ctx

@register.inclusion_tag('includes/iglesia_ajax_form.html', takes_context=True)
def iglesia_ajax(context):
	request = context['request']
	form_iglesia = IglesiaForm(request=request)
	ctx = {'form_iglesia': form_iglesia}
	return ctx

# from myapp.forms import IglesiaForm
# @register.inclusion_tag('includes/iglesia_ajax_form.html', takes_context=True)
# def iglesia_ajax(context):
#     request = context['request']
#     form_iglesia = IglesiaForm(request=request)
#     ctx = {'form_iglesia': form_iglesia}
#     return ctx

@register.inclusion_tag('nota_marginal/nota_marginal.html', takes_context=True)
def nota_marginal(context):
	form_nota=NotaMarginalForm()
	ctx = {'form_nota':form_nota}
	return ctx



