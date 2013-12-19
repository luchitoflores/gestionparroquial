# -*- coding:utf-8 -*-
from django import template
from sacramentos.forms import UsuarioPadreForm, PadreForm,PerfilUsuarioForm,NotaMarginalForm, UsuarioSecretariaForm, SecretariaForm
register = template.Library()

# @register.inclusion_tag('usuario/form_padre.html', takes_context=True)
# def padre(context):
# 	form_perfil_padre = PadreForm
# 	form_usuario = UsuarioForm
# 	ctx = {'form_perfil_padre':form_perfil_padre,'form_usuario':form_usuario}
# 	return ctx

@register.inclusion_tag('usuario/feligres.html', takes_context=True)
def feligres(context):
	form_perfil = PadreForm()
	form_usuario = UsuarioPadreForm()
	ctx = {'form_padre':form_perfil,'form_usuariopadre':form_usuario}
	return ctx

@register.inclusion_tag('usuario/secretaria.html', takes_context=True)
def secretaria(context):
	form_perfil = SecretariaForm()
	form_usuario = UsuarioSecretariaForm()
	ctx = {'form_padre':form_perfil,'form_usuariopadre':form_usuario}
	return ctx

@register.inclusion_tag('nota_marginal/nota_marginal.html', takes_context=True)
def nota_marginal(context):
	form_nota=NotaMarginalForm()
	ctx = {'form_nota':form_nota}
	return ctx


@register.inclusion_tag('direccion/direccion_form.html', takes_context=True)
def direccion(context):
	pass

