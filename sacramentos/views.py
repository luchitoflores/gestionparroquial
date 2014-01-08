# -*- coding:utf-8 -*-
# Create your views here.
import json
import csv
from datetime import datetime
from datetime import date
from django import forms
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sessions.models import Session
from django.forms.util import ErrorList
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render,get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
# Para los logs
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
 
from ho import pisa
import StringIO
import cgi

from sacramentos.models import (PerfilUsuario,
	Libro,Matrimonio,Bautismo,Eucaristia,Confirmacion,NotaMarginal,
	Parroquia, Intenciones,
	AsignacionParroquia, PeriodoAsignacionParroquia,
	ParametrizaDiocesis,ParametrizaParroquia,
	)

from sacramentos.forms import (
	UsuarioForm, UsuarioPadreForm, UsuarioSacerdoteForm, UsuarioAdministradorForm, UsuarioSecretariaForm,
	PerfilUsuarioForm, PadreForm, SacerdoteForm, AdministradorForm, AdminForm, SecretariaForm,
	EmailForm,
	MatrimonioForm,MatrimonioFormEditar,
	BautismoForm,BautismoFormEditar,
	EucaristiaForm,EucaristiaFormEditar,
	ConfirmacionForm,ConfirmacionFormEditar,
	LibroForm,NotaMarginalForm,
	DivErrorList,
	IntencionForm,
	ParroquiaForm, 
	AsignarParroquiaForm, PeriodoAsignacionParroquiaForm, PeriodoAsignacionParroquiaUpdateForm,
	AsignarSecretariaForm,
	ParametrizaDiocesisForm,ParametrizaParroquiaForm,
	ReporteIntencionesForm,ReporteSacramentosAnualForm,ReportePermisoForm,
	)

from ciudades.forms import DireccionForm
from ciudades.models import Canton, Provincia, Parroquia as ParroquiaCivil


@login_required(login_url='/login/')
@permission_required('sacramentos.add_feligres', login_url='/login/', raise_exception=permission_required)
def usuarioCreateView(request):
	if request.method == 'POST':
		form_usuario = UsuarioForm(request.POST)
		padre = PerfilUsuario.objects.padre()
		madre =  PerfilUsuario.objects.madre()
		form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
		

		if form_usuario.is_valid() and form_perfil.is_valid():
			feligres, created = Group.objects.get_or_create(name='Feligres')
			usuario = form_usuario.save(commit=False)
			perfil = form_perfil.save(commit=False)
			usuario.username = perfil.crear_username(usuario.first_name, usuario.last_name)
			usuario.set_password(usuario.username)
			usuario.save()
			usuario.groups.add(feligres)
			perfil.user = usuario
			perfil.save()
			LogEntry.objects.log_action(
				user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(perfil).pk,
            	object_id=perfil.id,
            	object_repr=unicode(perfil),
            	action_flag=ADDITION,
            	change_message="Creo un Usuario")
			messages.success(request, 'Creado exitosamente')
			return HttpResponseRedirect('/usuario')
			
		else:
			padre = request.POST.get('padre')
			madre =  request.POST.get('madre')

			if padre and madre:
				padre = PerfilUsuario.objects.filter(id=padre)
				madre = PerfilUsuario.objects.filter(id=madre)
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
			elif padre and not madre:
				padre = PerfilUsuario.objects.filter(id=padre)
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
			elif not padre and madre:
				madre = PerfilUsuario.objects.filter(id=madre)
				padre= PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)

			else:
				padre = PerfilUsuario.objects.none()
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST)
			
			messages.error(request, 'Uno o más datos no son válidos')
			ctx = {'form_usuario': form_usuario , 'form_perfil': form_perfil}
			return render(request, 'usuario/usuario_form.html', ctx)
	else:
		form_usuario = UsuarioForm()
		form_perfil = PerfilUsuarioForm(label_suffix=':')
		# form_perfil.fields['madre'] = forms.ModelChoiceField(queryset=PerfilUsuario.objects.female(), required=False, empty_label='--- Seleccione ---')
		# form_perfil.fields['padre'] = forms.ModelChoiceField(queryset=PerfilUsuario.objects.male(), required=False, empty_label='--- Seleccione ---')
		ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil}
		return render(request, 'usuario/usuario_form.html', ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_feligres', login_url='/login/', 
	raise_exception=permission_required)
def edit_usuario_view(request,pk):
	perfil= get_object_or_404(PerfilUsuario, pk=pk)
	user= perfil.user

	if perfil.user.groups.filter(name='Administrador').exists() or perfil.user.groups.filter(name='Sacerdote').exists():
		raise Http404

	if request.method == 'POST':
		padre = PerfilUsuario.objects.padre()
		madre =  PerfilUsuario.objects.madre()
		form_usuario = UsuarioForm(request.POST,instance=user)
		form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
		

		if form_usuario.is_valid() and form_perfil.is_valid():
			form_usuario.save()
			form_perfil.save()
			LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(perfil).pk,
            	object_id=perfil.id,
            	object_repr=unicode(perfil),
            	action_flag=CHANGE,
            	change_message="Usuario actualizado")
			messages.success(request, 'Actualizado exitosamente')
			return HttpResponseRedirect('/usuario')
		else:
			if perfil.padre and perfil.madre:
				padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
				madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
			elif perfil.padre and not perfil.madre:
				padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
			elif not perfil.padre and perfil.madre:
				madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
				padre= PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)

			else:
				padre = PerfilUsuario.objects.none()
				madre = PerfilUsuario.objects.none()
				form_perfil = PerfilUsuarioForm(padre, madre, request.POST,instance=perfil)
			
			messages.error(request, 'Uno o más campos no son válidos')
			ctx = {'form_usuario': form_usuario,'form_perfil':form_perfil, 'perfil':perfil}
			return render(request, 'usuario/usuario_form.html', ctx)

	else:
		if perfil.padre and perfil.madre:
			padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
			madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
			form_perfil = PerfilUsuarioForm(padre, madre, instance=perfil)
		elif perfil.padre and not perfil.madre:
			padre = PerfilUsuario.objects.filter(user__id=perfil.padre.user.id)
			form_perfil = PerfilUsuarioForm(padre, instance=perfil)
		elif not perfil.padre and perfil.madre:
			madre = PerfilUsuario.objects.filter(user__id=perfil.madre.user.id)
			padre= PerfilUsuario.objects.none()
			form_perfil = PerfilUsuarioForm(padre, madre, instance=perfil)

		else:
			form_perfil = PerfilUsuarioForm(instance=perfil)

		form_usuario = UsuarioForm(instance=user)
		
									
	ctx = {'form_usuario': form_usuario,'form_perfil':form_perfil, 'perfil':perfil}
	return render(request, 'usuario/usuario_form.html', ctx)

class UsuarioListView(ListView):
	model=PerfilUsuario
	template_name="usuario/usuario_list.html"
	queryset = PerfilUsuario.objects.feligres()

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_feligres', 
		login_url='/login/', raise_exception=permission_required))
	# @method_decorator(permission_required('auth.change_user', 
	# 	login_url='/login/', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(UsuarioListView, self).dispatch(*args, **kwargs)

@login_required(login_url='/login/')
@permission_required('sacramentos.add_administrador', login_url='/login/', 
	raise_exception=permission_required)

def administrator_create_view(request):
	template_name= 'usuario/admin_form.html'
	success_url = '/administrador/'
	if request.method == 'POST':
		form = AdminForm(request.POST)
		form.fields['administrador'].queryset = PerfilUsuario.objects.all()
		perfil = request.POST.get('administrador')

		persona = PerfilUsuario.objects.get(pk=perfil)
		usuario = persona.user
		if not usuario.email:
			form.errors["administrador"] = ErrorList([u'El usuario no tiene correo electrónico. '])
		
		is_staff = request.POST.get('is_staff')
		
		if form.is_valid():
			administrador, created = Group.objects.get_or_create(name='Administrador')
			usuario.groups.add(administrador)
			if is_staff:
				usuario.is_staff=True
			else:
				usuario.is_staff=False
			
			usuario.save()	
			return HttpResponseRedirect(success_url)
		else:
			form_email = EmailForm()
			administrador = persona
			form.fields['administrador'].queryset = PerfilUsuario.objects.filter(pk=administrador.id)
			ctx = {'form': form, 'form_email': form_email, 'administrador':administrador}
			return render(request, template_name, ctx) 	
	else:
		form = AdminForm()
		# form_email = EmailForm()
		ctx = {'form': form}
		return render(request, template_name, ctx) 


def administrador_create_view(request):
	template_name = 'usuario/administrador_form.html' 
	success_url = '/administrador/'
	
	if request.method == 'POST':
		form_sacerdote = AdministradorForm(request.POST)
		form_usuario = UsuarioAdministradorForm(request.POST)

		if form_sacerdote.is_valid() and form_usuario.is_valid():
			administrador, created = Group.objects.get_or_create(name='Administrador')
			usuario = form_usuario.save(commit= False) 
			sacerdote = form_sacerdote.save(commit=False)
			usuario.username= sacerdote.crear_username(usuario.first_name, usuario.last_name)
			usuario.set_password(usuario.username)
			usuario.save()
			usuario.groups.add(administrador)
			sacerdote.user =usuario
			sacerdote.save()
			LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(sacerdote).pk,
            	object_id=sacerdote.id,
            	object_repr=unicode(sacerdote),
            	action_flag=ADDITION,
            	change_message="Creo un administrador")
			messages.success(request, 'Creado exitosamente')
			return HttpResponseRedirect(success_url)

		else:
			messages.error(request, 'Uno o más datos son inválidos')
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
			return render(request, template_name, ctx)

	else:
		form_sacerdote = AdministradorForm()
		form_usuario = UsuarioAdministradorForm()
		ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_administrador', login_url='/login/', 
	raise_exception=permission_required)
def administrador_update_view(request, pk):
	sacerdote = get_object_or_404(PerfilUsuario, pk=pk)
	template_name = 'usuario/administrador_form.html' 
	success_url = '/administrador/'

	if request.method == 'POST':
		staff = request.POST.get('is_staff')
		form_sacerdote = AdministradorForm(request.POST, instance=sacerdote)
		form_usuario = UsuarioAdministradorForm(request.POST, instance=sacerdote.user)

		if request.user == sacerdote.user and not staff:
			form_usuario.errors["is_staff"] = ErrorList([u'No está permitido que Ud se desactive del sistema.'])

		if form_sacerdote.is_valid() and form_usuario.is_valid():
			usuario = form_usuario.save() 
			sacerdote = form_sacerdote.save()
			if not usuario.is_staff:
				#Esta linea de código permite desloguear a un usuario de manera remota
				[s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == usuario.id]
			LogEntry.objects.log_action(
           		user_id=request.user.id,
           		content_type_id=ContentType.objects.get_for_model(sacerdote).pk,
           		object_id=sacerdote.id,
           		object_repr=unicode(sacerdote),
           		action_flag=CHANGE,
           		change_message="Administrador actualizado")
			messages.success(request, 'Actualizado exitosamente')
			return HttpResponseRedirect(success_url)

		else:
			messages.error(request, 'Uno o más datos no son válidos')
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario, 'object': sacerdote}
			return render(request, template_name, ctx)

	else:
		form_sacerdote = AdministradorForm(instance=sacerdote)
		form_usuario = UsuarioAdministradorForm(instance=sacerdote.user)
		ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario, 'object': sacerdote}
		return render(request, template_name, ctx)



class AdministradorListView(ListView):
	model=PerfilUsuario
	template_name="usuario/administrador_list.html"
	#queryset = PerfilUsuario.objects.administrador()
	def get_queryset(self):
		user = self.request.user
		return PerfilUsuario.objects.administrador()

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_administrador', 
		login_url='/login/', raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(AdministradorListView, self).dispatch(*args, **kwargs)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_secretaria', login_url='/login/', 
	raise_exception=permission_required)
def secretaria_update_view(request, pk):
	secretaria = get_object_or_404(PerfilUsuario, pk=pk)

	if not secretaria.user.groups.filter(name='Secretaria').exists():
		raise Http404

	template_name = 'usuario/secretaria_form.html'
	success_url = '/asignar/secretaria/'
	if request.method == 'POST':
		perfil_form = SecretariaForm(request.POST, instance=secretaria)
		usuario_form = UsuarioSecretariaForm(request.POST, instance=secretaria.user)
		
		if usuario_form.is_valid() and perfil_form.is_valid():
			perfil = perfil_form.save()
			usuario = usuario_form.save()
			LogEntry.objects.log_action(
           		user_id=request.user.id,
           		content_type_id=ContentType.objects.get_for_model(secretaria).pk,
           		object_id=secretaria.id,
           		object_repr=unicode(secretaria),
           		action_flag=CHANGE,
           		change_message="Secretaria actualizado")
			messages.success(request, 'Actualizado exitosamente')			
			return HttpResponseRedirect(success_url)
		else:
			messages.error(request, 'Uno o más campos no son válidos %s %s' % (perfil_form.errors, usuario_form.errors))
			ctx = {'form_usuario': usuario_form, 'form_perfil':perfil_form, 'object': secretaria}
			return render(request,template_name, ctx)
	else:
		perfil_form = SecretariaForm(instance=secretaria)
		usuario_form = UsuarioSecretariaForm(instance=secretaria.user)
		ctx = {'form_usuario': usuario_form, 'form_perfil':perfil_form, 'object': secretaria}
		return render(request, template_name, ctx)

		
@login_required(login_url='/login/')
@permission_required('sacramentos.add_sacerdote', login_url='/login/', 
	raise_exception=permission_required)
def sacerdote_create_view(request):
	template_name = 'usuario/sacerdote_form.html' 
	success_url = '/sacerdote/'
	
	if request.method == 'POST':
		form_sacerdote = SacerdoteForm(request.POST)
		form_usuario = UsuarioSacerdoteForm(request.POST)
		
		if form_sacerdote.is_valid() and form_usuario.is_valid():
			sacerdotes, created = Group.objects.get_or_create(name='Sacerdote')
			usuario = form_usuario.save(commit= False) 
			sacerdote = form_sacerdote.save(commit=False)
			usuario.username= sacerdote.crear_username(usuario.first_name, usuario.last_name)
			usuario.set_password(usuario.username)
			usuario.save()
			usuario.groups.add(sacerdotes)
			sacerdote.user =usuario
			sacerdote.sexo = 'm'
			sacerdote.profesion = 'Sacerdote'
			sacerdote.estado_civil = 's'
			sacerdote.save()
			LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(sacerdote).pk,
            	object_id=sacerdote.id,
            	object_repr=unicode(sacerdote),
            	action_flag=ADDITION,
            	change_message="Creo un sacerdote")
			messages.success(request, 'Creado exitosamente')
			return HttpResponseRedirect(success_url)

		else:
			messages.error(request, 'Uno o más datos son inválidos')
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
			return render(request, template_name, ctx)

	else:
		form_sacerdote = SacerdoteForm()
		form_usuario = UsuarioSacerdoteForm()
		ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_sacerdote', login_url='/login/', 
	raise_exception=permission_required)
def sacerdote_update_view(request, pk):
	sacerdote = get_object_or_404(PerfilUsuario, pk=pk)
	template_name = 'usuario/sacerdote_form.html' 
	success_url = '/sacerdote/'
	
	if not sacerdote.user.groups.filter(name='Sacerdote').exists():
		raise Http404
	else: 
		if request.method == 'POST':
			form_sacerdote = SacerdoteForm(request.POST, instance=sacerdote)
			form_usuario = UsuarioSacerdoteForm(request.POST, instance=sacerdote.user)
			
			if form_sacerdote.is_valid() and form_usuario.is_valid():
				usuario = form_usuario.save() 
				sacerdote = form_sacerdote.save()
				LogEntry.objects.log_action(
            		user_id=request.user.id,
            		content_type_id=ContentType.objects.get_for_model(sacerdote).pk,
            		object_id=sacerdote.id,
            		object_repr=unicode(sacerdote),
            		action_flag=CHANGE,
            		change_message="Sacerdote actualizado")
				messages.success(request, 'Actualizado exitosamente')
				return HttpResponseRedirect(success_url)

			else:
				messages.error(request, 'Uno o más datos son inválidos')
				ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario, 'object': sacerdote}
				return render(request, template_name, ctx)

		else:
			form_sacerdote = SacerdoteForm(instance=sacerdote)
			form_usuario = UsuarioSacerdoteForm(instance=sacerdote.user)
			ctx = {'form_sacerdote': form_sacerdote, 'form_usuario':form_usuario, 'object': sacerdote}
			return render(request, template_name, ctx)


class SacerdoteListView(ListView):
	model = PerfilUsuario
	template_name = 'usuario/sacerdote_list.html'
	queryset = PerfilUsuario.objects.sacerdote()

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_sacerdote', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(SacerdoteListView, self).dispatch(*args, **kwargs)






# Vistas para admin libros

# @login_required(login_url='/login/')
# @permission_required('sacramentos.add_libro', login_url='/login/', 
# 	raise_exception=permission_required)
# def libro_create_view(request):
# 	if(request.method=='POST'):
# 		form_libro=LibroForm(request.POST)
# 		if form_libro.is_valid():
# 			libro=form_libro.save(commit=False)
# 			estado=libro.estado
# 			tipo=libro.tipo_libro
# 			numero=libro.numero_libro
# 			asignacion = AsignacionParroquia.objects.get(
# 				persona__user=request.user)
# 			libro.parroquia = asignacion.parroquia

# 			try:
# 				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo,
# 					parroquia=asignacion.parroquia)
# 				if(estado != consulta.estado and tipo!=consulta.tipo_libro):
# 					libro_numero=Libro.objects.get(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia)
# 					if numero!=libro_numero.numero_libro:
# 						libro.save()
# 						LogEntry.objects.log_action(
# 							user_id=request.user.id,
# 							content_type_id=ContentType.objects.get_for_model(libro).pk,
# 							object_id=libro.id,
# 							object_repr=unicode(libro),
# 							action_flag=ADDITION,
# 							change_message="Creo un libro")
# 						messages.success(request, 'Creado exitosamente')
# 						return HttpResponseRedirect('/libro')
# 					else:
# 						messages.error(request,'Ya existe un libro con ese numero')
					

# 				elif(estado != consulta.estado and tipo==consulta.tipo_libro):
# 					libro_numero=Libro.objects.get(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia)
# 					if numero!=libro_numero.numero_libro:
# 						libro.save()
# 						LogEntry.objects.log_action(
# 							user_id=request.user.id,
# 							content_type_id=ContentType.objects.get_for_model(libro).pk,
# 							object_id=libro.id,
# 							object_repr=unicode(libro.tipo_libro),
# 							action_flag=ADDITION,
# 							change_message="Creo un libro")
# 						messages.success(request, 'Creado exitosamente')
# 						return HttpResponseRedirect('/libro')
# 					else:
# 						messages.error(request,'Ya existe un libro con ese numero')

# 				elif(estado == consulta.estado and tipo!=consulta.tipo_libro):
# 					libro_numero=Libro.objects.get(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia)
# 					if numero!=libro_numero.numero_libro:
# 						libro.save()
# 						LogEntry.objects.log_action(
# 							user_id=request.user.id,
# 							content_type_id=ContentType.objects.get_for_model(libro).pk,
# 							object_id=libro.id,
# 							object_repr=unicode(libro.tipo_libro),
# 							action_flag=ADDITION,
# 							change_message="Creo un libro")
# 						messages.success(request, 'Creado exitosamente')
# 						return HttpResponseRedirect('/libro')
# 					else:
# 						messages.error(request,'Ya existe un libro con ese numero')	
# 				else:

# 					messages.error(request,'Ya existe un libro abierto, cierrelo '+
# 						'y vuela a crear')
# 					# messages.add_message(request,messages.WARNING,
# 					# 	{'Libro':'Ya existe un libro abierto, cierrelo y vuela a crear'})

# 			except ObjectDoesNotExist:
# 				libro.save()
# 				LogEntry.objects.log_action(
#             			user_id=request.user.id,
#             			content_type_id=ContentType.objects.get_for_model(libro).pk,
#             			object_id=libro.id,
#             			object_repr=unicode(libro),
#             			action_flag=ADDITION,
#             			change_message="Creo un libro")
# 				messages.success(request, 'Creado exitosamente')
# 				return HttpResponseRedirect('/libro')
# 		else:
# 			messages.error(request,'Uno o mas datos son invalidos')
# 			# messages.add_message(request,messages.WARNING,{'libro':form_libro.errors})
# 	else:
# 		form_libro=LibroForm()
# 	ctx={'form_libro':form_libro}
# 	return render(request,'libro/libro_form.html',ctx)



@login_required(login_url='/login/')
@permission_required('sacramentos.add_libro', login_url='/login/', 
	raise_exception=permission_required)
def libro_create_view(request):
	if(request.method=='POST'):
		form_libro=LibroForm(request.POST)
		asignacion = AsignacionParroquia.objects.get(
				persona__user=request.user,periodoasignacionparroquia__estado=True)
		parroquia=asignacion.parroquia
		numero1=request.POST.get('numero_libro')
		tipo2=request.POST.get('tipo_libro')
		if numero1:
			libro2=''
			try:
				libro2 = Libro.objects.get(tipo_libro=tipo2, numero_libro=numero1,
					parroquia=asignacion.parroquia)
			except ObjectDoesNotExist:
				print 'hola'

			if libro2:
				form_libro.errors["numero_libro"] = ErrorList([u'Ya existe un libro con este numero'])

		if form_libro.is_valid():
			libro=form_libro.save(commit=False)
			estado=libro.estado
			tipo=libro.tipo_libro
			numero=libro.numero_libro
			
			libro.parroquia = asignacion.parroquia

			try:
				consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo,
					parroquia=asignacion.parroquia)
				if(estado != consulta.estado and tipo!=consulta.tipo_libro):
					libro.save()
					LogEntry.objects.log_action(
						user_id=request.user.id,
						content_type_id=ContentType.objects.get_for_model(libro).pk,
						object_id=libro.id,
						object_repr=unicode(libro),
						action_flag=ADDITION,
						change_message="Creo un libro")
					messages.success(request, 'Creado exitosamente')
					return HttpResponseRedirect('/libro')
					

				elif(estado != consulta.estado and tipo==consulta.tipo_libro):
					libro.save()
					LogEntry.objects.log_action(
						user_id=request.user.id,
						content_type_id=ContentType.objects.get_for_model(libro).pk,
						object_id=libro.id,
						object_repr=unicode(libro.tipo_libro),
						action_flag=ADDITION,
						change_message="Creo un libro")
					messages.success(request, 'Creado exitosamente')
					return HttpResponseRedirect('/libro')
					
				
				elif(estado == consulta.estado and tipo!=consulta.tipo_libro):
					libro.save()
					LogEntry.objects.log_action(
						user_id=request.user.id,
						content_type_id=ContentType.objects.get_for_model(libro).pk,
						object_id=libro.id,
						object_repr=unicode(libro.tipo_libro),
						action_flag=ADDITION,
						change_message="Creo un libro")
					messages.success(request, 'Creado exitosamente')
					return HttpResponseRedirect('/libro')
					
				else:
					messages.error(request,'Ya existe un libro abierto, cierrelo '+
						'y vuela a crear')
					ctx={'form_libro':form_libro}
					return render(request,'libro/libro_form.html',ctx)
					
			except ObjectDoesNotExist:
				libro.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
            		content_type_id=ContentType.objects.get_for_model(libro).pk,
            		object_id=libro.id,
            		object_repr=unicode(libro),
            		action_flag=ADDITION,
            		change_message="Creo un libro")
				messages.success(request, 'Creado exitosamente')
				return HttpResponseRedirect('/libro')
				

		else:
			print('FORM INVALIDO ')
			ctx={'form_libro':form_libro}
			messages.error(request,ctx)
			return render(request,'libro/libro_form.html',ctx)
	else:
		form_libro=LibroForm()
	ctx={'form_libro':form_libro}
	return render(request,'libro/libro_form.html',ctx)

# class LibroUpdateView(UpdateView):
# 	model = Libro
# 	form_class=LibroForm
# 	template_name = 'libro/libro_form.html'
# 	success_url = '/libro/'

@login_required(login_url='/login/')
@permission_required('sacramentos.change_libro', login_url='/login/', 
	raise_exception=permission_required)
def libro_update_view(request,pk):
	libros=get_object_or_404(Libro,pk=pk)
	try:
		parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, 
			asignacion__parroquia=libros.parroquia, estado=True).asignacion.parroquia
		if(request.method=='POST'):
			form_libro=LibroForm(request.POST,instance=libros)
			asignacion = AsignacionParroquia.objects.get(
				persona__user=request.user,periodoasignacionparroquia__estado=True)
			numero1=request.POST.get('numero_libro')
			tipo2=request.POST.get('tipo_libro')
			if numero1:
				libro2 = Libro.objects.filter(tipo_libro=tipo2, numero_libro=numero1,parroquia=asignacion.parroquia).exclude(pk=pk)
				if libro2:
					form_libro.errors["numero_libro"] = ErrorList([u'Ya existe un libro con este numero'])
			if(form_libro.is_valid()):
				libro=form_libro.save(commit=False)
				estado=libro.estado
				tipo=libro.tipo_libro
				numero=libro.numero_libro
				try:
					consulta=Libro.objects.get(estado='Abierto',tipo_libro=tipo,
						parroquia=asignacion.parroquia)
					if (libro.id == consulta.id):
						if libro.estado == consulta.estado:
							l=Libro.objects.filter(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia).exclude(pk=pk)
							if not l:
								libro.save()
								LogEntry.objects.log_action(
									user_id=request.user.id,
									content_type_id=ContentType.objects.get_for_model(libro).pk,
									object_id=libro.id,
									object_repr=unicode(libro),
									action_flag=CHANGE,
									change_message="Libro actualizado")
								messages.success(request, 'Actualizado exitosamente')
								# form_libro._errors["numero_libro"] = ErrorList([u"error message goes here"])
								# print 'errores de libro %s' % form_libro.errors
								return HttpResponseRedirect('/libro')
							else:
								messages.error(request,'Ya existe el numero de libro')
						else:
							l=Libro.objects.filter(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia).exclude(pk=pk)
							if not l:
								libro.save()
								LogEntry.objects.log_action(
            						user_id=request.user.id,
            						content_type_id=ContentType.objects.get_for_model(libro).pk,
            						object_id=libro.id,
            						object_repr=unicode(libro.tipo_libro),
            						action_flag=CHANGE,
            						change_message="Libro actualizado")
								messages.success(request, 'Actualizado exitosamente')

								return HttpResponseRedirect('/libro')
							else:
								messages.error(request,'Ya existe el numero de libro')
						
					else:
						if(estado != consulta.estado and tipo!=consulta.tipo_libro):
							l=Libro.objects.filter(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia).exclude(pk=pk)
							if not l:
								libro.save()
								LogEntry.objects.log_action(
            					user_id=request.user.id,
            					content_type_id=ContentType.objects.get_for_model(libro).pk,
            					object_id=libro.id,
            					object_repr=unicode(libro.tipo_libro),
            					action_flag=CHANGE,
            					change_message="Libro actualizado")
								messages.success(request, 'Actualizado exitosamente')
								return HttpResponseRedirect('/libro')
							else:
								messages.error(request,'Ya existe el numero de libro')
						
						elif(estado != consulta.estado and tipo==consulta.tipo_libro):
							l=Libro.objects.filter(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia).exclude(pk=pk)
							if not l:	
								libro.save()
								LogEntry.objects.log_action(
            						user_id=request.user.id,
            						content_type_id=ContentType.objects.get_for_model(libro).pk,
            						object_id=libro.id,
            						object_repr=unicode(libro.tipo_libro),
            						action_flag=CHANGE,
            						change_message="Libro actualizado")
								messages.success(request, 'Actualizado exitosamente')
								return HttpResponseRedirect('/libro')
							else:
								messages.error(request,'Ya existe el numero del libro')
													
						else:

							messages.error(request,'Ya existe un libro abierto, cierrelo '+
								'y vuela a crear')
						
				except ObjectDoesNotExist:
					l=Libro.objects.filter(tipo_libro=tipo, numero_libro=numero,parroquia=asignacion.parroquia).exclude(pk=pk)
					if not l:
						libro.save()
						LogEntry.objects.log_action(
							user_id=request.user.id,
            				content_type_id=ContentType.objects.get_for_model(libro).pk,
            				object_id=libro.id,
            				object_repr=unicode(libro.tipo_libro),
            				action_flag=CHANGE,
            				change_message="Libro actualizado")
						messages.success(request, 'Actualizado exitosamente')
						return HttpResponseRedirect('/libro')
					else:
						messages.error(request,'Ya existe el numero del libro')
						ctx={'form_libro':form_libro,'object':libros}
						return render(request,'libro/libro_form.html',ctx)
			else:
			
				ctx={'form_libro':form_libro,'object':libros}
				messages.error(request,'Los datos del formulario son incorrectos %s'%form_libro.errors)
				return render(request,'libro/libro_form.html',ctx)
		else:
			form_libro=LibroForm(instance=libros)
		ctx={'form_libro':form_libro,'object':libros}
		return render(request,'libro/libro_form.html',ctx)
	except ObjectDoesNotExist:
		raise PermissionDenied


class LibroListView(ListView):
	model = Libro
	template_name = 'libro/libro_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user)
			queryset = Libro.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];


	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_libro', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(LibroListView, self).dispatch(*args, **kwargs)
	

# VISTAS PARA ADMIN MATRIMONIO

@login_required(login_url='/login/')
@permission_required('sacramentos.add_matrimonio', login_url='/login/', 
	raise_exception=permission_required)
def matrimonio_create_view(request):
	usuario=request.user
	
	if(request.method=='POST'):
		novio = PerfilUsuario.objects.padre()
		novia = PerfilUsuario.objects.madre()
		celebrante=PerfilUsuario.objects.sacerdote()
		form_matrimonio=MatrimonioForm(usuario,novio,novia,celebrante,request.POST)

		novio_post =  get_object_or_404(PerfilUsuario, pk= request.POST.get('novio'))
		novia_post =  get_object_or_404(PerfilUsuario, pk= request.POST.get('novia'))

		if novio_post.estado_civil=='c':
			form_matrimonio.errors["novio"] = ErrorList([u'El feligrés seleccionado ya está casado'])
		
		if novia_post.estado_civil=='c':
			form_matrimonio.errors["novia"] = ErrorList([u'El feligrés seleccionado ya está casada'])
		
		if form_matrimonio.is_valid():
			matrimonio=form_matrimonio.save(commit=False)
			matrimonio.tipo_sacramento='Matrimonio'
			novio=matrimonio.novio
			novia=matrimonio.novia
			libro=matrimonio.libro
			asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
				periodoasignacionparroquia__estado=True)
			m=Matrimonio.objects.filter(libro=libro,parroquia=asignacion.parroquia).count()
			if  (novio.estado_civil!='c') and (novia.estado_civil!='c'):
							
				if (novio.sexo=='m' and novia.sexo=='f'):
					try:
						p=ParametrizaParroquia.objects.get(parroquia=asignacion.parroquia)
											
					except ObjectDoesNotExist:
						raise PermissionDenied
					if m==0:
						matrimonio.pagina=p.pagina
						matrimonio.numero_acta=p.numero_acta
						novio.estado_civil='c'
						novia.estado_civil='c'
						novio.save()
						novia.save()
						matrimonio.novio=novio
						matrimonio.novia=novia
						matrimonio.parroquia = asignacion.parroquia
						matrimonio.vigente=True
						matrimonio.save()
						LogEntry.objects.log_action(
							user_id=request.user.id,
							content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
							object_id=matrimonio.id,
							object_repr=unicode(matrimonio),
							action_flag=ADDITION,
							change_message='Se creo matrimonio')
						messages.success(request,'Creado exitosamente')
						return HttpResponseRedirect('/matrimonio')
					else:
						ultimo_matrimonio=Matrimonio.objects.filter(parroquia=asignacion.parroquia).latest('created')
						num=ultimo_matrimonio.numero_acta
						pagina=ultimo_matrimonio.pagina
						matrimonio.numero_acta=num+1
						matrimonio.pagina=pagina+1
						novio.estado_civil='c'
						novia.estado_civil='c'
						novio.save()
						novia.save()
						matrimonio.novio=novio
						matrimonio.novia=novia
						matrimonio.parroquia = asignacion.parroquia
						matrimonio.vigente=True
						matrimonio.save()
						LogEntry.objects.log_action(
							user_id=request.user.id,
							content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
							object_id=matrimonio.id,
							object_repr=unicode(matrimonio),
							action_flag=ADDITION,
							change_message='Se creo matrimonio')
						messages.success(request,'Creado exitosamente')
						return HttpResponseRedirect('/matrimonio')
				else:
					messages.error(request,'No se puen casar novios con el mismo sexo')
			else:
				messages.error(request,'Uno de los novios ya esta casado')
				
		else:
			novio = request.POST.get('novio')
			novia = request.POST.get('novia')
			celebrante =  request.POST.get('celebrante')
			if novio and novia and celebrante:
			    novio = PerfilUsuario.objects.filter(id=novio)
			    novia = PerfilUsuario.objects.filter(id=novia)
			    celebrante = PerfilUsuario.objects.filter(id=celebrante)
			    form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif novio and novia and not celebrante:
				novio = PerfilUsuario.objects.filter(id=novio)
				novia = PerfilUsuario.objects.filter(id=novia)
				celebrante = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif not novio and novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novio= PerfilUsuario.objects.none()
				novia = PerfilUsuario.objects.filter(id=novia)
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif novio and not novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.filter(id=novio)
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif novio and not novia and not celebrante:
				celebrante = PerfilUsuario.objects.none()
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.filter(id=novio)
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			elif not novio and novia and not celebrante:
				celebrante = PerfilUsuario.objects.none()
				novia= PerfilUsuario.objects.filter(id=novia)
				novio = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)	
			elif not novio and not novia and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				novia= PerfilUsuario.objects.none()
				novio = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio, novia,celebrante, request.POST)
			else:
				novio = PerfilUsuario.objects.none()
				novia = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				form_matrimonio = MatrimonioForm(usuario,novio,novia, celebrante, request.POST)

			if novio_post.estado_civil=='c':
				form_matrimonio.errors["novio"] = ErrorList([u'El feligrés elegido ya está casado'])
			
			if novia_post.estado_civil=='c':
				form_matrimonio.errors["novia"] = ErrorList([u'La feligrés elegida ya está casada'])
			
			messages.error(request,'Los datos del formulario son incorrectos')
			ctx={'form_matrimonio':form_matrimonio}
			return render(request,'matrimonio/matrimonio_form.html',ctx)
		
	else:

		form_matrimonio=MatrimonioForm(usuario)
		
	ctx={'form_matrimonio':form_matrimonio}
	return render(request,'matrimonio/matrimonio_form.html',ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_matrimonio', login_url='/login/', 
	raise_exception=permission_required)
def matrimonio_update_view(request,pk):
	usuario=request.user
	matrimonio=get_object_or_404(Matrimonio,pk=pk)
	notas=NotaMarginal.objects.filter(matrimonio=matrimonio)
	try:
		parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, 
			asignacion__parroquia=matrimonio.parroquia, estado=True).asignacion.parroquia
	
		if request.method == 'POST':
			novio = PerfilUsuario.objects.padre()
			novia = PerfilUsuario.objects.madre()
			celebrante=PerfilUsuario.objects.sacerdote()
			form_matrimonio = MatrimonioFormEditar(usuario,novio,novia,celebrante,request.POST,
				instance=matrimonio)
			if form_matrimonio.is_valid():
				matrimonio=form_matrimonio.save(commit=False)
				novio=matrimonio.novio
				novia=matrimonio.novia
				if (novio.sexo=='m' and novia.sexo=='f'):
					novio.estado_civil='c'
					novia.estado_civil='c'
					novio.save()
					novia.save()
					matrimonio.novio=novio
					matrimonio.novia=novia
					asignacion = AsignacionParroquia.objects.get(persona__user=request.user)
					matrimonio.parroquia = asignacion.parroquia
					matrimonio.vigente=True
					matrimonio.save()
					LogEntry.objects.log_action(
						user_id=request.user.id,
	            		content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
	            		object_id=matrimonio.id,
	            		object_repr=unicode(matrimonio),
	            		action_flag=CHANGE,
	            		change_message='Matrimonio actualizado')
					messages.success(request,'Actualizado exitosamente')
					return HttpResponseRedirect('/matrimonio')
				else:
					messages.info(request,'No se puen casar novios con el mismo sexo')
			
			else:
				novio = request.POST.get('novio')
				novia = request.POST.get('novia')
				celebrante =  request.POST.get('celebrante')

				if novio and novia and celebrante:
					novio = PerfilUsuario.objects.filter(id=novio)
					novia = PerfilUsuario.objects.filter(id=novia)
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
						instance=matrimonio)
				elif novio and novia and not celebrante:
					novio = PerfilUsuario.objects.filter(id=novio)
					novia = PerfilUsuario.objects.filter(id=novia)
					celebrante = PerfilUsuario.objects.none()
					form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
						instance=matrimonio)
				elif not novio and novia and celebrante:
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					novio= PerfilUsuario.objects.none()
					novia = PerfilUsuario.objects.filter(id=novia)
					form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
						instance=matrimonio)
				elif novio and not novia and celebrante:
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					novia= PerfilUsuario.objects.none()
					novio = PerfilUsuario.objects.filter(id=novio)
					form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
						instance=matrimonio)
				elif novio and not novia and not celebrante:
					celebrante = PerfilUsuario.objects.none()
					novia= PerfilUsuario.objects.none()
					novio = PerfilUsuario.objects.filter(id=novio)
					form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, request.POST,
						instance=matrimonio)

				else:
					novio = PerfilUsuario.objects.none()
					novio = PerfilUsuario.objects.none()
					celebrante = PerfilUsuario.objects.none()
					form_matrimonio = MatrimonioFormEditar(usuario,novio,novia, celebrante, request.POST,
						instance=matrimonio)
				messages.error(request, 'Los datos del formulario son incorrectos')
				ctx = {'form_matrimonio': form_matrimonio,'notas':notas,'object':matrimonio}
				return render(request,'matrimonio/matrimonio_form.html', ctx)
			
		else:
			if matrimonio.novio and matrimonio.novia and matrimonio.celebrante:
				novio = PerfilUsuario.objects.filter(user__id=matrimonio.novio.user.id)
				novia = PerfilUsuario.objects.filter(user__id=matrimonio.novia.user.id)
				celebrante = PerfilUsuario.objects.filter(user__id=matrimonio.celebrante.user.id)
				form_matrimonio = MatrimonioFormEditar(usuario,novio, novia,celebrante, instance=matrimonio)
										
		ctx = {'form_matrimonio': form_matrimonio,'notas':notas,'object':matrimonio}
		return render(request, 'matrimonio/matrimonio_form.html', ctx)
	except ObjectDoesNotExist:
		raise PermissionDenied


@login_required(login_url='/login/')
@permission_required('sacramentos.delete_matrimonio', login_url='/login/', 
	raise_exception=permission_required)
def matrimonio_vigencia_view(request,pk):
	usuario = request.user
	matrimonio=Matrimonio.objects.get(pk=pk)	
	if request.method == 'POST':
		novio=matrimonio.novio
		novia=matrimonio.novia
		novio.estado_civil='v'
		novia.estado_civil='v'
		novio.save()
		novia.save()
		matrimonio.vigente=False
		matrimonio.save()
		LogEntry.objects.log_action(
			user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
            object_id=matrimonio.id,
            object_repr=unicode(matrimonio),
            action_flag=DELETION,
            change_message='Dado de baja matrimonio')
		messages.success(usuario, 'Se ha quitado la vigencia con exito')
		return HttpResponseRedirect('/matrimonio')

	else:
		form = MatrimonioForm(usuario,instance=matrimonio)
		matrimonio.vigente=False
		matrimonio.save()
	
	ctx = {'form': form}
	return render(request,'matrimonio/matrimonio_list.html', ctx)


@login_required(login_url='/login/')
def matrimonio_ajax_view(request):
	exito = False
	matrimonio=Matrimonio.objects.all()
	list_matrimonios= list()
	for m in matrimonio:
		novio=u'%s' % m.novio.user.get_full_name()
		novia=u'%s' % m.novia.user.get_full_name()
		list_matrimonios.append({ 'id': m.pk, 'novio':novio,'novia':novia})
	ctx={'list_matrimonios':list_matrimonios, 'exito':exito}
	return HttpResponse(json.dumps(ctx), content_type='application/json')


class MatrimonioNoVigenteListView(ListView):
	model = Matrimonio
	template_name = 'matrimonio/matrimonio_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(
				persona__user=self.request.user,periodoasignacionparroquia__estado=True)
			queryset = Matrimonio.objects.filter(parroquia=asignacion.parroquia,vigente=False)
			return queryset
		except: 
			return [];
	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_matrimonio', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(MatrimonioNoVigenteListView, self).dispatch(*args, **kwargs)


class MatrimonioListView(ListView):
	model = Matrimonio
	template_name = 'matrimonio/matrimonio_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(
				persona__user=self.request.user,periodoasignacionparroquia__estado=True)

			queryset = Matrimonio.objects.filter(parroquia=asignacion.parroquia,vigente=True)
			return queryset
		except: 
			return [];

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_matrimonio', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(MatrimonioListView, self).dispatch(*args, **kwargs)



# VISTAS PARA ADMIN DE BAUTISMO

@login_required(login_url='/login/')
@permission_required('sacramentos.add_bautismo', login_url='/login/', 
	raise_exception=permission_required)
def bautismo_create_view(request):
	usuario=request.user
	if(request.method == 'POST' ):
		bautizado=PerfilUsuario.objects.feligres()
		celebrante=PerfilUsuario.objects.sacerdote()
		formBautismo=BautismoForm(usuario,bautizado,celebrante,request.POST)
	
		if (formBautismo.is_valid()):
			bautismo=formBautismo.save(commit=False)
			bautismo.tipo_sacramento =  u'Bautismo'
			libro=bautismo.libro
			asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
				periodoasignacionparroquia__estado=True)
			b=Bautismo.objects.filter(libro=libro, parroquia=asignacion.parroquia).count()
			try:
				p=ParametrizaParroquia.objects.get(parroquia=asignacion.parroquia)
				

			except ObjectDoesNotExist:
				raise PermissionDenied

			if b==0:
				bautismo.pagina=p.pagina
				bautismo.numero_acta=p.numero_acta
				bautismo.parroquia = asignacion.parroquia
				bautismo.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(bautismo).pk,
					object_id=bautismo.id,
					object_repr=unicode(bautismo),
					action_flag=ADDITION,
					change_message='Se creo bautismo')
				messages.success(request,'Creado exitosamente')
				return HttpResponseRedirect('/bautismo')
			else:
				ultimo_bautismo=Bautismo.objects.filter(libro=libro,parroquia=asignacion.parroquia).latest('created')
				num=ultimo_bautismo.numero_acta
				pagina=ultimo_bautismo.pagina

				bautismo.numero_acta=num+1
				if bautismo.numero_acta%2 == 0:
					bautismo.pagina=pagina
				else:
					bautismo.pagina=pagina+1
				bautismo.parroquia = asignacion.parroquia
				bautismo.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(bautismo).pk,
					object_id=bautismo.id,
					object_repr=unicode(bautismo),
					action_flag=ADDITION,
					change_message='Se creo bautismo')
				messages.success(request,'Creado exitosamente')
				return HttpResponseRedirect('/bautismo')
		else:
			bautizado = request.POST.get('bautizado')
			celebrante =  request.POST.get('celebrante')

			if bautizado and celebrante:
				bautizado = PerfilUsuario.objects.filter(id=bautizado)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)
			elif bautizado and not celebrante:
				bautizado = PerfilUsuario.objects.filter(id=bautizado)
				celebrante = PerfilUsuario.objects.none()
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)
			elif not bautizado and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				bautizado= PerfilUsuario.objects.none()
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)

			else:
				bautizado = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				formBautismo = BautismoForm(usuario,bautizado, celebrante, request.POST)

			
			messages.error(request,'Los datos del formulario son incorrectos')
			ctx={'formBautismo':formBautismo}
			return render (request,'bautismo/bautismo_form.html',ctx)
	else:
		
		formBautismo=BautismoForm(usuario)
		# form_nota=NotaMarginalForm()
	ctx={'formBautismo':formBautismo}
	return render (request,'bautismo/bautismo_form.html',ctx)



def mostrar():
	return self.model.objects.filter()


@login_required(login_url='/login/')
@permission_required('sacramentos.change_bautismo', login_url='/login/', 
	raise_exception=permission_required)
def bautismo_update_view(request,pk):
	usuario=request.user
	bautismo= get_object_or_404(Bautismo, pk=pk)
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	try:

		parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, 
			asignacion__parroquia=bautismo.parroquia, estado=True).asignacion.parroquia
			
		if request.method == 'POST':
			bautizado = PerfilUsuario.objects.all()
			celebrante=PerfilUsuario.objects.sacerdote()
			bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante,request.POST,instance=bautismo)
			# form_nota=NotaMarginalForm(request.POST,instance=nota)
			if bautismo_form.is_valid():
				bautismo_form.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
		           	content_type_id=ContentType.objects.get_for_model(bautismo).pk,
		           	object_id=bautismo.id,
		           	object_repr=unicode(bautismo),
		           	action_flag=CHANGE,
		           	change_message='Bautismo actualizado')
				messages.success(request,'Actualizado exitosamente')
				return HttpResponseRedirect('/bautismo')
			else:
				bautizado = request.POST.get('bautizado')
				celebrante = request.POST.get('celebrante')
				if bautizado and celebrante:
					bautizado = PerfilUsuario.objects.filter(id=bautizado)
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, request.POST,
						instance=bautismo)
				elif(bautizado and not celebrante):
					bautizado = PerfilUsuario.objects.filter(id=bautizado)
					celebrante=PerfilUsuario.objects.none()
					bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, request.POST,
						instance=bautismo)
				elif(celebrante and not bautizado):
					bautizado=PerfilUsuario.objects.none()
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, request.POST,
						instance=bautismo)
			
				else:
					celebrante = PerfilUsuario.objects.none()
					bautizado = PerfilUsuario.objects.none()
					bautismo_form = BautismoFormEditar(usuario, bautizado,celebrante,request.POST, 
							instance=bautismo)
				
				messages.error(request, "Los datos del formulario son incorrectos")
				ctx = {'formBautismo': bautismo_form,'notas':notas,'object':bautismo}
				return render(request, 'bautismo/bautismo_form.html', ctx)
				
		else:
			if bautismo.bautizado and bautismo.celebrante:
				bautizado = PerfilUsuario.objects.filter(user__id=bautismo.bautizado.user.id)
				celebrante=PerfilUsuario.objects.filter(user__id=bautismo.celebrante.user.id)
				bautismo_form = BautismoFormEditar(usuario,bautizado,celebrante, instance=bautismo)
			else:
				bautismo_form = BautismoFormEditar(instance=bautismo)
													
			ctx = {'formBautismo': bautismo_form,'notas':notas,'object':bautismo}
			return render(request, 'bautismo/bautismo_form.html', ctx)
		
	except ObjectDoesNotExist:
		raise PermissionDenied


class BautismoListView(ListView):
	model=Bautismo
	template_name='bautismo/bautismo_list.html'
	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user,
				periodoasignacionparroquia__estado=True)
			queryset = Bautismo.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_bautismo', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(BautismoListView, self).dispatch(*args, **kwargs)

# VISTAS PARA ADMIN DE EUCARISTIA


@login_required(login_url='/login/')
@permission_required('sacramentos.add_eucaristia', login_url='/login/', 
	raise_exception=permission_required)
def eucaristia_create_view(request):
	usuario=request.user
	if request.method == 'POST':
		feligres=PerfilUsuario.objects.feligres()
		celebrante=PerfilUsuario.objects.sacerdote()
		form_eucaristia=EucaristiaForm(usuario,feligres,celebrante,request.POST)
		if form_eucaristia.is_valid():
			eucaristia=form_eucaristia.save(commit=False)
			tipo_sacramento=u'Eucaristia'
			eucaristia.tipo_sacramento=tipo_sacramento
			libro=eucaristia.libro
			asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
				periodoasignacionparroquia__estado=True)
			e=Eucaristia.objects.filter(libro=libro,parroquia=asignacion.parroquia).count()
			try:
				p=ParametrizaParroquia.objects.get(parroquia=asignacion.parroquia)
				
			except ObjectDoesNotExist:
				raise PermissionDenied
			if e==0:
				eucaristia.pagina=p.pagina
				eucaristia.numero_acta=p.numero_acta
				eucaristia.parroquia = asignacion.parroquia
				eucaristia.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(eucaristia).pk,
					object_id=eucaristia.id,
					object_repr=unicode(eucaristia),
					action_flag=ADDITION,
					change_message='Se creo eucaristia')
				messages.success(request,'Creado exitosamente')
				return HttpResponseRedirect('/eucaristia')

			else:
				ultimo_eucaristia=Eucaristia.objects.filter(libro=libro,parroquia=asignacion.parroquia).latest('created')
				num=ultimo_eucaristia.numero_acta
				pagina=ultimo_eucaristia.pagina

				eucaristia.numero_acta=num+1
				if eucaristia.numero_acta%2 == 0:
					eucaristia.pagina=pagina
				else:
					eucaristia.pagina=pagina+1
				eucaristia.parroquia = asignacion.parroquia
				eucaristia.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(eucaristia).pk,
					object_id=eucaristia.id,
					object_repr=unicode(eucaristia),
					action_flag=ADDITION,
					change_message='Se creo eucaristia')
				messages.success(request,'Creado exitosamente')
				return HttpResponseRedirect('/eucaristia')
		else:
			feligres = request.POST.get('feligres')
			celebrante =  request.POST.get('celebrante')

			if feligres and celebrante:
				feligres = PerfilUsuario.objects.filter(id=feligres)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)
			elif feligres and not celebrante:
				feligres = PerfilUsuario.objects.filter(id=feligres)
				celebrante = PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)
			elif not feligres and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				feligres= PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)

			else:
				feligres = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				form_eucaristia = EucaristiaForm(usuario,feligres, celebrante, request.POST)
			messages.error(request,"Los datos del formulario son incorrectos")
			ctx={'form_eucaristia':form_eucaristia}
			return render(request,'eucaristia/eucaristia_form.html',ctx)
	else:
		form_eucaristia=EucaristiaForm(usuario)

	ctx={'form_eucaristia':form_eucaristia}
	return render(request,'eucaristia/eucaristia_form.html',ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_eucaristia', login_url='/login/', 
	raise_exception=permission_required)
def eucaristia_update_view(request,pk):
	usuario=request.user
	eucaristia=get_object_or_404(Eucaristia,pk=pk)
	try:
		parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, 
			asignacion__parroquia=eucaristia.parroquia, estado=True).asignacion.parroquia
		if(request.method == 'POST'):
			feligres= PerfilUsuario.objects.feligres()
			celebrante=PerfilUsuario.objects.sacerdote()
			form_eucaristia=EucaristiaFormEditar(usuario,feligres,celebrante,request.POST,instance=eucaristia)
			if(form_eucaristia.is_valid()):
				form_eucaristia.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
            		content_type_id=ContentType.objects.get_for_model(eucaristia).pk,
            		object_id=eucaristia.id,
            		object_repr=unicode(eucaristia),
            		action_flag=CHANGE,
            		change_message='Eucaristia actualizada')
				messages.success(request,'Actualizado exitosamente')
				return HttpResponseRedirect('/eucaristia')
			else:

				feligres = request.POST.get('feligres')
				celebrante = request.POST.get('celebrante')
				if feligres and celebrante:
					feligres = PerfilUsuario.objects.filter(id=feligres)
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					form_eucaristia = EucaristiaFormEditar(usuario,feligres,celebrante, request.POST,
						instance=eucaristia)
				elif(feligres and not celebrante):
					feligres = PerfilUsuario.objects.filter(id=feligres)
					celebrante=PerfilUsuario.objects.none()
					form_eucaristia = EucaristiaFormEditar(usuario,feligres, celebrante,request.POST,
						instance=eucaristia)
				elif(celebrante and not feligres):
					feligres=PerfilUsuario.objects.none()
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					form_eucaristia = EucaristiaFormEditar(usuario,feligres,celebrante, request.POST,
						instance=eucaristia)
			
				else:
					celebrante = PerfilUsuario.objects.none()
					feligres = PerfilUsuario.objects.none()
					form_eucaristia = EucaristiaFormEditar(usuario, feligres,celebrante,request.POST, 
						instance=eucaristia)

				messages.error(request,"Los datos del formulario son incorrectos")
				ctx={'form_eucaristia':form_eucaristia, 'object':eucaristia}
				return render(request,'eucaristia/eucaristia_form.html',ctx)
		
		else:
			if eucaristia.feligres and eucaristia.celebrante:
				feligres = PerfilUsuario.objects.filter(user__id=eucaristia.feligres.user.id)
				celebrante=PerfilUsuario.objects.filter(user__id=eucaristia.celebrante.user.id)
				form_eucaristia = EucaristiaFormEditar(usuario,feligres,celebrante, instance=eucaristia)
		
		
		ctx={'form_eucaristia':form_eucaristia, 'object':eucaristia}
		return render(request,'eucaristia/eucaristia_form.html',ctx)
	except ObjectDoesNotExist:
		raise PermissionDenied



class EucaristiaListView(ListView):
	model=Eucaristia
	template_name='eucaristia/eucaristia_list.html'
	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user,
				periodoasignacionparroquia__estado=True)
			queryset = Eucaristia.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_eucaristia', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(EucaristiaListView, self).dispatch(*args, **kwargs)

# VISTAS PARA ADMIN DE CONFIRMACION

@login_required(login_url='/login/')
@permission_required('sacramentos.add_confirmacion', login_url='/login/', 
	raise_exception=permission_required)
def confirmacion_create_view(request):
	usuario=request.user
	confirmado=PerfilUsuario.objects.feligres()
	celebrante=PerfilUsuario.objects.sacerdote()
	if(request.method == 'POST'):
		form_confirmacion=ConfirmacionForm(usuario,confirmado,celebrante,request.POST)
		if(form_confirmacion.is_valid()):
			confirmacion=form_confirmacion.save(commit=False)
			confirmacion.tipo_sacramento='Confirmacion'
			libro=confirmacion.libro
			asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
				periodoasignacionparroquia__estado=True)
			c=Confirmacion.objects.filter(libro=libro,parroquia=asignacion.parroquia).count()
			try:
				p=ParametrizaParroquia.objects.get(parroquia=asignacion.parroquia)
				
			except ObjectDoesNotExist:
				raise PermissionDenied

			if c==0:
				confirmacion.pagina=p.pagina
				confirmacion.numero_acta=p.numero_acta
				confirmacion.parroquia = asignacion.parroquia
				confirmacion.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(confirmacion).pk,
					object_id=confirmacion.id,
					object_repr=unicode(confirmacion),
					action_flag=ADDITION,
					change_message='Se creo confirmacion')
				messages.success(request,'Creado exitosamente')
				return HttpResponseRedirect('/confirmacion')
				
			else:
				ultima_confirmacion=Confirmacion.objects.filter(libro=libro,parroquia=asignacion.parroquia).latest('created')
				num=ultima_confirmacion.numero_acta
				pagina=ultima_confirmacion.pagina

				confirmacion.numero_acta=num+1
				if confirmacion.numero_acta%2 == 0:
					confirmacion.pagina=pagina
				else:
					confirmacion.pagina=pagina+1
				confirmacion.parroquia = asignacion.parroquia
				confirmacion.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(confirmacion).pk,
					object_id=confirmacion.id,
					object_repr=unicode(confirmacion),
					action_flag=ADDITION,
					change_message='Se creo bautismo')
				messages.success(request,'Creado exitosamente')
				return HttpResponseRedirect('/confirmacion')
		else:
			confirmado = request.POST.get('confirmado')
			celebrante =  request.POST.get('celebrante')

			if confirmado and celebrante:
				confirmado = PerfilUsuario.objects.filter(id=confirmado)
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				form_confirmacion = ConfirmacionForm(usuario,confirmado, celebrante, request.POST)
			elif confirmado and not celebrante:
				confirmado = PerfilUsuario.objects.filter(id=confirmado)
				celebrante = PerfilUsuario.objects.none()
				form_confirmacion = EucaristiaForm(usuario,confirmado, celebrante, request.POST)
			elif not confirmado and celebrante:
				celebrante = PerfilUsuario.objects.filter(id=celebrante)
				confirmado= PerfilUsuario.objects.none()
				form_confirmacion = EucaristiaForm(usuario,confirmado, celebrante, request.POST)

			else:
				confirmado = PerfilUsuario.objects.none()
				celebrante = PerfilUsuario.objects.none()
				form_confirmacion = EucaristiaForm(usuario,confirmado, celebrante, request.POST)

			messages.error(request,"Los datos del formulario son incorrectos")
			ctx={'form_confirmacion':form_confirmacion}
			return render(request,'confirmacion/confirmacion_form.html',ctx)
			
	else:
		form_confirmacion=ConfirmacionForm(usuario)
	ctx={'form_confirmacion':form_confirmacion}
	return render(request,'confirmacion/confirmacion_form.html',ctx)




@login_required(login_url='/login/')
@permission_required('sacramentos.change_confirmacion', login_url='/login/', 
	raise_exception=permission_required)
def confirmacion_update_view(request,pk):
	usuario=request.user
	confirmacion=get_object_or_404(Confirmacion,pk=pk)
	try:
		parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, 
			asignacion__parroquia=confirmacion.parroquia, estado=True).asignacion.parroquia
		if(request.method == 'POST'):
			confirmado=PerfilUsuario.objects.feligres()
			celebrante=PerfilUsuario.objects.sacerdote()
			form_confirmacion=ConfirmacionFormEditar(usuario,confirmado,celebrante,request.POST,
				instance=confirmacion)
			if(form_confirmacion.is_valid()):
				form_confirmacion.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
           			content_type_id=ContentType.objects.get_for_model(confirmacion).pk,
            		object_id=confirmacion.id,
            		object_repr=unicode(confirmacion),
            		action_flag=CHANGE,
            		change_message='Confirmacion actualizado')
				messages.success(request,'Actualizado exitosamente')
				return HttpResponseRedirect('/confirmacion')
			else:
				confirmado = request.POST.get('confirmado')
				celebrante = request.POST.get('celebrante')
				if confirmado and celebrante:
					confirmado = PerfilUsuario.objects.filter(id=confirmado)
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, request.POST,
						instance=confirmacion)
				elif(confirmado and not celebrante):
					confirmado = PerfilUsuario.objects.filter(id=confirmado)
					celebrante=PerfilUsuario.objects.none()
					form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, request.POST,
						instance=confirmacion)
				elif(celebrante and not confirmado):
					confirmado=PerfilUsuario.objects.none()
					celebrante = PerfilUsuario.objects.filter(id=celebrante)
					form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, request.POST,
						instance=confirmacion)
		
				else:
					celebrante = PerfilUsuario.objects.none()
					confirmado = PerfilUsuario.objects.none()
					form_confirmacion = ConfirmacionFormEditar(usuario, confirmado,celebrante,request.POST, 
						instance=confirmacion)
			

				messages.error(request,"Los datos del formulario son incorrectos")
				ctx={'form_confirmacion':form_confirmacion,'object':confirmacion}
				return render(request,'confirmacion/confirmacion_form.html',ctx)
		else:
			if confirmacion.confirmado and confirmacion.celebrante:
				confirmado = PerfilUsuario.objects.filter(user__id=confirmacion.confirmado.user.id)
				celebrante = PerfilUsuario.objects.filter(user__id=confirmacion.celebrante.user.id)
				form_confirmacion = ConfirmacionFormEditar(usuario,confirmado,celebrante, instance=confirmacion)
			else:
				form_confirmacion = EucaristiaFormEditar(instance=confirmacion)

		
		ctx={'form_confirmacion':form_confirmacion,'object':confirmacion}
		return render(request,'confirmacion/confirmacion_form.html',ctx)
	except ObjectDoesNotExist:
		raise PermissionDenied


class ConfirmacionListView(ListView):
	model=Confirmacion
	template_name='confirmacion/confirmacion_list.html'

	def get_queryset(self):
		try:
			asignacion = AsignacionParroquia.objects.get(persona__user=self.request.user,
				periodoasignacionparroquia__estado=True)
			queryset = Confirmacion.objects.filter(parroquia=asignacion.parroquia)
			return queryset
		except: 
			return [];

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_confirmacion', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ConfirmacionListView, self).dispatch(*args, **kwargs)



#Vistas para crear una parroquia
@login_required(login_url='/login/')
@permission_required('sacramentos.add_parroquia', login_url='/login/', 
	raise_exception=permission_required)
def parroquia_create_view(request):
	"""
    Permite crear una parroquia con su respectiva direccion de domicilio,
    provincia, canton y parroquia civil

    """
	template_name = 'parroquia/parroquia_form.html'
	success_url = '/parroquia/'
	if request.method== 'POST':
		form_parroquia = ParroquiaForm(request.POST)
		canton = Canton.objects.all()
		parroquia_civil = ParroquiaCivil.objects.all()
		form_direccion = DireccionForm(canton, parroquia_civil, request.POST)
		if form_parroquia.is_valid() and form_direccion.is_valid():
			parroquia = form_parroquia.save(commit=False)
			direccion = form_direccion.save()
			parroquia.direccion = direccion
			parroquia.save()
			LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(parroquia).pk,
            	object_id=parroquia.id,
            	object_repr=unicode(parroquia),
            	action_flag=ADDITION,
            	change_message="Creo una parroquia")
			return HttpResponseRedirect(success_url)
		else:
			ctx = {'form_parroquia': form_parroquia, 'form_direccion':form_direccion}
			# messages.error(request, ctx)
			messages.error(request, 'Los datos del formulario son incorrectos')
			return render(request, template_name, ctx)
	else:
		form_parroquia = ParroquiaForm()
		form_direccion = DireccionForm()
		ctx = {'form_parroquia': form_parroquia, 'form_direccion':form_direccion}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_parroquia', login_url='/login/', 
	raise_exception=permission_required)
def parroquia_update_view(request, pk):
	template_name = 'parroquia/parroquia_form.html'
	success_url = '/parroquia/'
	parroquia = get_object_or_404(Parroquia, pk = pk)
	direccion = parroquia.direccion
	print u'direccion.- %s' % direccion

	if request.method == 'POST':
		form_parroquia = ParroquiaForm(request.POST, instance=parroquia)
		canton = Canton.objects.all()
		parroquia_civil = ParroquiaCivil.objects.all()
		form_direccion = DireccionForm(canton, parroquia_civil, request.POST, instance=direccion)
		if form_parroquia.is_valid() and form_direccion.is_valid():
			form_parroquia.save()
			form_direccion.save()
			LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(parroquia).pk,
            	object_id=parroquia.id,
            	object_repr=unicode(parroquia),
            	action_flag=CHANGE,
            	change_message="Parroquia actualizada")
			# parroquia = form_parroquia.save(commit=False)
			# direccion = form_direccion.save()
			# parroquia.direccion = direccion
			# parroquia.save()
			return HttpResponseRedirect(success_url)
		else:
			ctx = {'form_parroquia':form_parroquia, 'form_direccion':form_direccion}
			messages.error(request, 'Los datos del formulario son incorrectos')
			return render(request, template_name, ctx)
	else:
		canton = Canton.objects.filter(provincia=parroquia.direccion.provincia)
		parroquia_civil = ParroquiaCivil.objects.filter(canton=parroquia.direccion.canton)
		form_parroquia = ParroquiaForm(instance=parroquia)
		form_direccion = DireccionForm(instance=direccion, canton = canton, parroquia=parroquia_civil)
		ctx = {'form_parroquia': form_parroquia, 'form_direccion':form_direccion,'object':parroquia}
		return render(request, template_name, ctx)

class ParroquiaListView(ListView):
	model= Parroquia
	template_name = 'parroquia/parroquia_list.html'

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('sacramentos.change_parroquia', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ParroquiaListView, self).dispatch(*args, **kwargs)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_intenciones', login_url='/login/', 
	raise_exception=permission_required)
def intencion_create_view(request):
	template_name = 'intencion/intencion_form.html'
	success_url = '/intencion/'

	if not 'parroquia' in request.session:
		raise PermissionDenied

	if request.method == 'POST':
		form_intencion = IntencionForm(request.POST)
		if form_intencion.is_valid():
			fecha = request.POST.get('fecha')
			hora = request.POST.get('hora')
			individual = request.POST.get('individual')
			intencion = form_intencion.save(commit=False)
			try:
				asignacion = AsignacionParroquia.objects.get(persona__user=request.user, periodoasignacionparroquia__estado=True)
				parroquia = asignacion.parroquia
				intencion_unica = Intenciones.objects.filter(fecha=fecha, hora=hora, parroquia=parroquia, individual=True)
				intenciones_colectivas = Intenciones.objects.filter(fecha=fecha, hora=hora, parroquia=parroquia)
				if intencion_unica:
					messages.error(request, u'No se puede puede crear una intención, porque ya existe una intención única para el dia y hora indicado')
					ctx = {'form': form_intencion}
					return render(request, template_name, ctx)
				elif intenciones_colectivas and individual:
					messages.error(request, u'No se puede puede crear una intención única, porque ya existen intenciones colectivas para el dia y hora indicado')
					ctx = {'form': form_intencion, 'object': intencion}
					return render(request, template_name, ctx)
				else:
					# messages.success(request, 'Creado exitosamente: %s' %individual)
					intencion.parroquia = asignacion.parroquia
					intencion.save()
					LogEntry.objects.log_action(
	            	user_id=request.user.id,
	            	content_type_id=ContentType.objects.get_for_model(intencion).pk,
	            	object_id=intencion.id,
	            	object_repr=unicode(intencion),
	            	action_flag=ADDITION,
	            	change_message="Creo una intencion")
					messages.success(request, 'Creado exitosamente')
					return HttpResponseRedirect(success_url)
			except ObjectDoesNotExist:
				raise PermissionDenied
		else:
			messages.error(request, u'Los datos del formulario son incorrectos')
			ctx = {'form': form_intencion}
			return render(request, template_name, ctx)
	else:
		form_intencion = IntencionForm()
		ctx = {'form': form_intencion}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_intenciones', login_url='/login/', 
	raise_exception=permission_required)
def intencion_edit_view(request, pk):
	intencion = get_object_or_404(Intenciones, pk=pk)
	try:
		periodo_asignacion = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, estado=True, asignacion__parroquia=intencion.parroquia)
		template_name = 'intencion/intencion_form.html'
		success_url = '/intencion/'
		if request.method == 'POST':
			form_intencion = IntencionForm(request.POST, instance=intencion)
			if form_intencion.is_valid():
				fecha = request.POST.get('fecha')
				hora = request.POST.get('hora')
				individual = request.POST.get('individual')
				intencion_unica = Intenciones.objects.filter(fecha=fecha, hora=hora, parroquia=intencion.parroquia, individual=True).exclude(pk=pk)
				intenciones_colectivas = Intenciones.objects.filter(fecha=fecha, hora=hora, parroquia=intencion.parroquia).exclude(pk=pk)
				if intencion_unica:
					messages.error(request, u'No se puede puede actualizar la intención a única, porque ya existe una intención única para el dia y hora indicado')
					ctx = {'form': form_intencion, 'object': intencion}
					return render(request, template_name, ctx)
				elif intenciones_colectivas and individual:
					messages.error(request, u'No se puede puede actualizar la intención, porque ya existen intenciones colectivas para el dia y hora indicado')
					ctx = {'form': form_intencion, 'object': intencion}
					return render(request, template_name, ctx)
				else:
					intencion = form_intencion.save(commit=False)
					intencion.save()
					LogEntry.objects.log_action(
		            user_id=request.user.id,
		            content_type_id=ContentType.objects.get_for_model(intencion).pk,
		            object_id=intencion.id,
		            object_repr=unicode(intencion),
		            action_flag=ADDITION,
		            change_message="Creo una intencion")
					messages.success(request, 'Actualizado exitosamente')
					return HttpResponseRedirect(success_url)
			else:
				messages.error(request, u'Los datos del formulario son incorrectos')
				ctx = {'form': form_intencion}
				return render(request, template_name, ctx)
		else:
			form_intencion = IntencionForm(instance=intencion)
			ctx = {'form': form_intencion, 'object': intencion}
			return render(request, template_name, ctx)
	
	except ObjectDoesNotExist:
		raise PermissionDenied

@login_required(login_url='/login/')
@permission_required('sacramentos.change_intenciones', login_url='/login/', 
	raise_exception=permission_required)
def intencion_list_view(request):
	template_name= 'intencion/intencion_list.html'
	if 'parroquia' in request.session:
		parroquia = request.session['parroquia']
		object_list = Intenciones.objects.filter(parroquia=parroquia).order_by('fecha', 'hora')
		ctx = {'object_list': object_list} 
		return render(request, template_name, ctx)
	else:
		raise PermissionDenied

	# try:
	# 	parroquia = AsignacionParroquia.objects.get(persona__user=request.user, periodoasignacionparroquia__estado=True).parroquia
	# 	object_list = Intenciones.objects.filter(parroquia=parroquia).order_by('fecha', 'hora')
	# 	ctx = {'object_list': object_list} 
	# 	return render(request, template_name, ctx)
	# except ObjectDoesNotExist:
	# 	object_list = Intenciones.objects.all()
	# 	ctx = {'object_list': object_list} 
	# 	return render(request, template_name, ctx)

	
	

@login_required(login_url='/login/')
@permission_required('sacramentos.add_asignarsacerdote', login_url='/login/', 
	raise_exception=permission_required)
def asignar_parroquia_create(request):
	template_name = "parroquia/asignar_parroquia_form.html"
	success_url = '/parroquia/'
	parroquia = request.POST.get('parroquia')
	persona = request.POST.get('persona')
	# estado = self.request.POST.get('estado')
	# print persona


	if request.method == 'POST':
		form = AsignarParroquiaForm(request.POST)
		form_periodo = PeriodoAsignacionParroquiaForm(request.POST)
		if form.is_valid() and form_periodo.is_valid():
			
			try: 
				asignacion = AsignacionParroquia.objects.get(persona__id = persona, 
					parroquia__id = parroquia)
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(parroquia).pk,
            	object_id=parroquia.id,
            	object_repr=unicode(parroquia),
            	action_flag=ADDITION,
            	change_message="Asigno parroquia y sacerdote")
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()


				return HttpResponseRedirect(success_url)

			except ObjectDoesNotExist:
				asignacion = form.save()
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(parroquia).pk,
            	object_id=parroquia.id,
            	object_repr=unicode(parroquia),
            	action_flag=ADDITION,
            	change_message="Asigno parroquia y sacerdote")
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()
				return HttpResponseRedirect(success_url)

		else:
			messages.error(request, 'Los datos del formulario son incorrectos')
			ctx = {'form': form, 'form_periodo': form_periodo}
			# return render(request, template_name, ctx)
	else:
		form_periodo = PeriodoAsignacionParroquiaForm()
		form = AsignarParroquiaForm()
		ctx = {'form': form, 'form_periodo': form_periodo}
	return render(request, template_name, ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.add_asignarsacerdote', login_url='/login/', 
	raise_exception=permission_required)
def asignar_parroco_a_parroquia(request, pk):
	template_name = "parroquia/asignar_parroquia_form.html"
	success_url = '/parrocos/parroquia/%s/' % (pk)
	parroquia = get_object_or_404(Parroquia, pk=pk)
	persona = request.POST.get('persona')
	print parroquia
	parroquias = Parroquia.objects.filter(id=pk)
	queryset = Parroquia.objects.all()

	
	if request.method == 'POST':
		form = AsignarParroquiaForm(queryset, request.POST)
		form_periodo = PeriodoAsignacionParroquiaForm(request.POST)
		if form.is_valid() and form_periodo.is_valid():
			try: 
				asignacion = AsignacionParroquia.objects.get(persona__id = persona, 
					parroquia__id = parroquia.id)
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()
				LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(parroquia).pk,
            	object_id=parroquia.id,
            	object_repr=unicode(parroquia),
            	action_flag=ADDITION,
            	change_message="Asigno parroquia y sacerdote")
				return HttpResponseRedirect(success_url)

			except ObjectDoesNotExist:
				asignacion = form.save()
				periodo = form_periodo.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				user = PerfilUsuario.objects.get(pk=persona).user
				user.is_staff = True 
				user.save()
				LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(parroquia).pk,
            	object_id=parroquia.id,
            	object_repr=unicode(parroquia),
            	action_flag=ADDITION,
            	change_message="Asigno parroquia y sacerdote")
				return HttpResponseRedirect(success_url)

		else:
			form = AsignarParroquiaForm(parroquias, request.POST)
			messages.error(request, 'Los datos del formulario son incorrectos')
			ctx = {'form': form, 'form_periodo': form_periodo}
			return render(request, template_name, ctx)
	else:
		form = AsignarParroquiaForm(parroquias)
		form_periodo = PeriodoAsignacionParroquiaForm()
		ctx = {'form': form, 'form_periodo': form_periodo, 'object': parroquia}
		return render(request, template_name, ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_asignarsacerdote', login_url='/login/', 
	raise_exception=permission_required)
def asignar_parroquia_update(request, pk):
	template_name = "parroquia/asignar_parroquia_form.html"
	success_url = '/asignar/parroquia/'
	asignacion = get_objeFct_or_404(AsignacionParroquia, pk=pk)
	periodos = PeriodoAsignacionParroquia.objects.filter(asignacion__id=asignacion.id)

	if request.method == 'POST':
		persona = PerfilUsuario.objects.feligres()
		form = AsignarParroquiaForm(request.POST, instance=asignacion)
		form_periodo = periodos
		if form.is_valid() and form_periodo.is_valid():
			asignacion = form.save(commit=False)
			periodo = form_periodo.save()
			asignacion.periodo = periodo
			form.save()
			LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(asignacion).pk,
            	object_id=asignacion.id,
            	object_repr=unicode(asignacion),
            	action_flag=CHANGE,
            	change_message="Actualizado asignacion parroquia y sacerdote")
			return HttpResponseRedirect(success_url)
		else:
			messages.error(request, 'Los datos del formulario son incorrectos')
			ctx = {'form': form, 'form_periodo': form_periodo, 'object': asignacion.parroquia}
			# return render(request, template_name, ctx)
	else:
		form_periodo = periodos
		form = AsignarParroquiaForm(instance=asignacion)
		ctx = {'form': form, 'form_periodo': form_periodo, 'object': asignacion.parroquia}
	return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_asignarsacerdote', login_url='/login/', 
	raise_exception=permission_required)
def nuevo_periodo_asignacion(request, pk):
	template_name = 'parroquia/periodo_asignacion_form.html'
	asignacion = AsignacionParroquia.objects.get(id=pk)
	success_url = '/parroco/periodos/asignacion/%s/' % asignacion.id
	if request.method == 'POST':
		form = PeriodoAsignacionParroquiaForm(request.POST)
		if form.is_valid():
			estado = request.POST.get('estado')
			periodo_activo= PeriodoAsignacionParroquia.objects.filter(asignacion=asignacion, estado=True)
			periodo_activo_otra_parroquia = PeriodoAsignacionParroquia.objects.filter(asignacion__persona=asignacion.persona, estado=True).exclude(asignacion__parroquia=asignacion.parroquia)
			if periodo_activo:
				messages.error(request, 'El sacerdote ya posee un periodo activo')
				ctx = {'form': form, 'object':asignacion}
				return render(request, template_name, ctx)
				
			elif periodo_activo_otra_parroquia:
				messages.error(request, 'El sacerdote tiene un periodo activo en otra parroquia')
				ctx = {'form': form, 'object':asignacion}
				return render(request, template_name, ctx)

			else:
				periodo = form.save(commit=False)
				periodo.asignacion = asignacion
				periodo.save()
				if estado:
					user = PerfilUsuario.objects.get(pk=periodo.asignacion.persona.id).user
					user.is_staff = True
					user.save()
				else: 
					user = PerfilUsuario.objects.get(pk=periodo.asignacion.persona.id).user
					user.is_staff = False
					user.save()
				LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(periodo).pk,
            	object_id=periodo.id,
            	object_repr=unicode(periodo),
            	action_flag=ADDITION,
            	change_message="Creo periodo de asignacion")
				return HttpResponseRedirect(success_url)

		else:
			ctx = {'form': form, 'object':asignacion}
			return render(request, template_name, ctx)

	else:
		form = PeriodoAsignacionParroquiaForm()
		ctx = {'form': form, 'object':asignacion}
		return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_asignarsacerdote', login_url='/login/', 
	raise_exception=permission_required)
def parroco_periodos_asignacion_update(request, pk):
	periodo = get_object_or_404(PeriodoAsignacionParroquia, pk = pk)
	template_name = 'parroquia/periodo_asignacion_form.html'
	success_url = u'/parroco/periodos/asignacion/%s/' % periodo.asignacion.id

	if request.method == 'POST':
		estado = request.POST.get('estado')
		form = PeriodoAsignacionParroquiaUpdateForm(request.POST, instance=periodo)
		if form.is_valid():
			
			periodo_activo= PeriodoAsignacionParroquia.objects.filter(asignacion=periodo.asignacion, estado=True).exclude(id=periodo.id)
			periodo_activo_otra_parroquia = PeriodoAsignacionParroquia.objects.filter(asignacion__persona=periodo.asignacion.persona, estado=True).exclude(asignacion__parroquia=periodo.asignacion.parroquia)
			if periodo_activo:
				messages.error(request, 'Existen periodos activos')
				ctx = {'form': form, 'periodo':periodo, 'object': periodo.asignacion}
				return render(request, template_name, ctx)
			elif  periodo_activo_otra_parroquia:
				messages.error(request, 'El sacerdote tiene un periodo activo en otra parroquia')
				ctx = {'form': form, 'periodo':periodo, 'object': periodo.asignacion}
				return render(request, template_name, ctx)

			else:
				if estado:
					user = PerfilUsuario.objects.get(pk=periodo.asignacion.persona.id).user
					user.is_staff = True
					user.save()
				else: 
					user = PerfilUsuario.objects.get(pk=periodo.asignacion.persona.id).user
					user.is_staff = False
					user.save()
				form.save()
				LogEntry.objects.log_action(
            	user_id=request.user.id,
            	content_type_id=ContentType.objects.get_for_model(periodo).pk,
            	object_id=periodo.id,
            	object_repr=unicode(periodo),
            	action_flag=CHANGE,
            	change_message="Periodo asignacion actualizado") 
				return HttpResponseRedirect(success_url)
		else:
			ctx = {'form': form, 'periodo':periodo, 'object': periodo.asignacion}
			return render(request, template_name, ctx)

	else:
		form = PeriodoAsignacionParroquiaUpdateForm(instance=periodo)
		ctx = {'form': form, 'periodo':periodo, 'object': periodo.asignacion}
		return render(request, template_name, ctx)


# El pk que recibe es el id de una asignación

@login_required(login_url='/login/')
@permission_required('sacramentos.change_asignarsacerdote', login_url='/login/', 
	raise_exception=permission_required)
def parroco_periodos_asignacion_list(request, pk):
	template_name = "parroquia/parroco_periodos_asignacion_list.html"
	success_url = '/asignar/parroquia/'
	# parroquia = get_object_or_404(Parroquia, pk=pk)
	periodos = PeriodoAsignacionParroquia.objects.filter(asignacion__id=pk)
	asignacion = get_object_or_404(AsignacionParroquia, pk=pk)
	
	ctx = {'object_list': periodos, 'asignacion': asignacion}
	return render(request, template_name, ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_asignarsacerdote', login_url='/login/', 
	raise_exception=permission_required)
def asignar_parroco_list(request, pk):
	template_name = 'parroquia/asignar_parroquia_list.html'
	object_list = AsignacionParroquia.objects.filter(parroquia__id=pk, persona__user__groups__name='Sacerdote') 
	parroquia = get_object_or_404(Parroquia, pk=pk)
	ctx = {'object_list': object_list, 'parroquia':parroquia}
	return render(request, template_name, ctx)
	

@login_required(login_url='/login/')
@permission_required('sacramentos.add_asignarsecretaria', login_url='/login/')
def asignar_secretaria_create(request):
	template_name = "parroquia/asignar_secretaria_form.html"
	success_url = '/asignar/secretaria/'
	usuario = request.user
	try:
		parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, estado=True).asignacion.parroquia
		if request.method == 'POST':
			perfil = get_object_or_404(PerfilUsuario, pk= request.POST.get('persona'))
			persona = PerfilUsuario.objects.feligres()
			form = AsignarSecretariaForm(usuario, persona, request.POST.get('estado'), request.POST)
			form_periodo = PeriodoAsignacionParroquiaForm(request.POST)
			
			if form.is_valid() and form_periodo.is_valid():
				try:
					periodo_asignacion =  PeriodoAsignacionParroquia.objects.get(asignacion__persona=perfil, estado = True)
					messages.error(request, 'El usuario %s ya cuenta con una asignación activa' % perfil)
					ctx = {'form': form, 'form_periodo':form_periodo}
					return render(request, template_name, ctx)
				except ObjectDoesNotExist:
					try:
						asignacion =  PeriodoAsignacionParroquia.objects.get(asignacion__persona=perfil, estado = False, asignacion__parroquia=parroquia)
						messages.error(request, 'El usuario %s tiene un periodo desactivo, proceda a activarlo desde la lista de secretarios/as' % perfil)
						ctx = {'form': form, 'form_periodo':form_periodo}
						return render(request, template_name, ctx)
					except ObjectDoesNotExist: 
						asig=form.save()
						periodo = form_periodo.save(commit=False)
						periodo.asignacion= asig
						periodo.save()
						LogEntry.objects.log_action(
		            	user_id=request.user.id,
		            	content_type_id=ContentType.objects.get_for_model(asig).pk,
		            	object_id=asig.id,
		            	object_repr=unicode(asig),
		            	action_flag=ADDITION,
		            	change_message="Asigno parroquia y secretaria")
						persona_id = request.POST['persona']
						estado = request.POST.get('estado')
						if estado:
							user = PerfilUsuario.objects.get(pk=persona_id).user
							user.is_staff = True 
							user.save()
							secretaria, created = Group.objects.get_or_create(name='Secretaria')
							user.groups.add(secretaria)
						else:
							user = PerfilUsuario.objects.get(pk=persona_id).user
							user.is_staff = False
							user.save()
							secretaria, created = Group.objects.get_or_create(name='Secretaria')
							user.groups.add(secretaria)
						return HttpResponseRedirect(success_url)
			else:
				if request.POST.get('persona'):
					form_email = EmailForm()
					messages.error(request, 'Los datos del formulario son incorrectos')
					persona = PerfilUsuario.objects.get(id=request.POST.get('persona'))
					personas = PerfilUsuario.objects.filter(id=request.POST.get('persona'))
					form = AsignarSecretariaForm(usuario, personas, request.POST.get('estado'), request.POST)
					ctx = {'form': form, 'form_periodo': form_periodo, 'form_email': form_email, 'persona': }
					
				else: 
					messages.error(request, 'Uno o más cámpos son inválidos')
					persona = PerfilUsuario.objects.none()
					form = AsignarSecretariaForm(usuario, persona, request.POST.get('estado'), request.POST)
					ctx = {'form': form, 'form_periodo': form_periodo}
				return render(request, template_name, ctx)
				
		else:
			form = AsignarSecretariaForm(usuario)
			form_periodo = PeriodoAsignacionParroquiaForm()
			ctx = {'form': form, 'form_periodo': form_periodo}
		return render(request, template_name, ctx)
	except ObjectDoesNotExist:
		raise PermissionDenied

#El parámetro pk es el id de un periodo
@login_required(login_url='/login/')
@permission_required('sacramentos.change_asignarsecretaria', login_url='/login/', 
	raise_exception=permission_required)
def asignar_secretaria_update(request, pk):
	periodo = get_object_or_404(PeriodoAsignacionParroquia, pk=pk)
	template_name = "parroquia/asignar_secretaria_form.html"
	success_url = '/asignar/secretaria/'
	
	try: 
		parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, estado=True).asignacion.parroquia
	
		if periodo.asignacion.parroquia == parroquia and periodo.asignacion.persona.user != request.user:

			usuario = request.user
			if request.method == 'POST':
				persona = PerfilUsuario.objects.feligres()
				form = AsignarSecretariaForm(usuario, persona, periodo.asignacion.persona.user.is_staff, request.POST, instance=periodo.asignacion)
				form_periodo = PeriodoAsignacionParroquiaUpdateForm(request.POST, instance=periodo)
				if form.is_valid() and form_periodo.is_valid():
					persona_id = request.POST['persona']
					estado = request.POST.get('estado')
					if estado:
						user = PerfilUsuario.objects.get(pk=persona_id).user
						user.is_staff = True 
						user.save()
					else:
						user = PerfilUsuario.objects.get(pk=persona_id).user
						user.is_staff = False
						user.save()
					asig = form.save()
					periodo = form_periodo.save(commit=False)
					periodo.asignacion= asig
					periodo.save()
					LogEntry.objects.log_action(
		            	user_id=request.user.id,
		            	content_type_id=ContentType.objects.get_for_model(periodo.asignacion).pk,
		            	object_id=periodo.asignacion.id,
		            	object_repr=unicode(periodo.asignacion),
		            	action_flag=ADDITION,
		            	change_message="Asignacion parroquia y secretaria actualizado")
					return HttpResponseRedirect(success_url)
				else:
					if periodo.asignacion.persona:
						messages.error(request, 'Los datos del formulario son incorrectos') 
						persona = PerfilUsuario.objects.filter(user__id=periodo.asignacion.persona.user.id)
						form = AsignarSecretariaForm(usuario, persona, periodo.asignacion.persona.user.is_staff, request.POST, instance=periodo.asignacion)
					else:
						messages.error(request, 'Los datos del formulario son incorrectos %s' % form) 
						persona = PerfilUsuario.objects.none()
						form = AsignarSecretariaForm(usuario, persona, request.POST,  instance=periodo.asignacion)

					ctx = {'form': form, 'form_periodo': form_periodo, 'object':periodo}
					return render(request, template_name, ctx)
			else:
				if periodo.asignacion.persona:
					persona = PerfilUsuario.objects.filter(user__id=periodo.asignacion.persona.user.id)
					form = AsignarSecretariaForm(usuario, persona, periodo.asignacion.persona.user.is_staff, instance=periodo.asignacion)
				else:
					persona = PerfilUsuario.objects.none()
					form = AsignarSecretariaForm(usuario, persona, asignacion.persona.user.is_staff, instance=periodo.asignacion)
				
				form_periodo = PeriodoAsignacionParroquiaUpdateForm(instance=periodo)
				ctx = {'form': form, 'form_periodo':form_periodo, 'object':periodo}
				return render(request, template_name, ctx)
		else:
			raise PermissionDenied
	
	except ObjectDoesNotExist:
		messages.error(request, 'Usted no está asignado a ninguna parroquia') 
		return HttpResponseRedirect(success_url)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_asignarsecretaria', login_url='/login/', 
	raise_exception=permission_required)
def asignar_secretaria_list(request):
	template_name = 'parroquia/asignar_secretaria_list.html'
	try:
		parroquia  = PeriodoAsignacionParroquia.objects.get(estado=True, asignacion__persona__user=request.user).asignacion.parroquia
		object_list = PeriodoAsignacionParroquia.objects.filter(asignacion__parroquia=parroquia, asignacion__persona__user__groups__name='Secretaria')
		# object_list= AsignacionParroquia.objects.filter(parroquia=parroquia).exclude(persona__user__groups__name='Sacerdote')
		ctx = {'object_list': object_list, 'parroquia':parroquia}
		return render(request, template_name, ctx)
	except ObjectDoesNotExist:
		raise PermissionDenied

@login_required(login_url='/login/')
@permission_required('sacramentos.add_parametrizadiocesis', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_parametrizadiocesis', login_url='/login/', 
	raise_exception=permission_required)		
def parametriza_diocesis_create(request):
	p=ParametrizaDiocesis.objects.all()
	if p:
		for e in p:
			of=e
		direccion = of.direccion
		if request.method=='POST':
			
			form_parametriza = ParametrizaDiocesisForm(request.POST, instance=of)
			canton = Canton.objects.all()
			parroquia_civil = ParroquiaCivil.objects.all()
			form_direccion = DireccionForm(canton, parroquia_civil, request.POST, instance=direccion)
			if form_parametriza.is_valid() and form_direccion.is_valid():
				form_parametriza.save()
				form_direccion.save()
				LogEntry.objects.log_action(
	            	user_id=request.user.id,
	            	content_type_id=ContentType.objects.get_for_model(of).pk,
	            	object_id=of.id,
	            	object_repr=unicode(of),
	            	action_flag=CHANGE,
	            	change_message="Parametriza Diocesis actualizada")
				
				return HttpResponseRedirect('/home/')
			else:
				ctx = {'form_parametriza':form_parametriza, 'form_direccion':form_direccion}
				messages.error(request,'Los datos del formulario son incorrectos')
				return render(request, 'parametriza/parametriza_form.html', ctx)
		else:
			canton = Canton.objects.filter(provincia=of.direccion.provincia)
			parroquia_civil = ParroquiaCivil.objects.filter(canton=of.direccion.canton)
			form_parametriza = ParametrizaDiocesisForm(instance=of)
			form_direccion = DireccionForm(instance=direccion, canton = canton, parroquia=parroquia_civil)
			ctx = {'form_parametriza': form_parametriza, 'form_direccion':form_direccion,'object':of}
			return render(request, 'parametriza/parametriza_form.html', ctx)


	else:
		if(request.method=='POST'):
			form_parametriza=ParametrizaDiocesisForm(request.POST)
			canton=Canton.objects.all()
			parroquia_civil=ParroquiaCivil.objects.all()
			form_direccion=DireccionForm(canton,parroquia_civil,request.POST)
			if form_parametriza.is_valid() and form_direccion.is_valid():
				parametriza=form_parametriza.save(commit=False)
				direccion=form_direccion.save()
				parametriza.direccion=direccion
				parametriza.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(parametriza).pk,
					object_id=parametriza.id,
					object_repr=unicode(parametriza),
					action_flag=ADDITION,
					change_message="Creo una parametriza diocesis"
					)
				return HttpResponseRedirect('/home/')
			else:
				ctx={'form_parametriza':form_parametriza,'form_direccion':form_direccion}
				messages.error(request,'Los datos del formulario son incorrectos')
				return render(request,'parametriza/parametriza_form.html',ctx)
		else:
			form_parametriza = ParametrizaDiocesisForm()
			form_direccion = DireccionForm()
			ctx = {'form_parametriza': form_parametriza, 'form_direccion':form_direccion}
			return render(request, 'parametriza/parametriza_form.html', ctx)
			
@login_required(login_url='/login/')
@permission_required('sacramentos.add_parametrizaparroquia', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_parametrizaparroquia', login_url='/login/', 
	raise_exception=permission_required)
def parametriza_parroquia_create(request):
	usuario=request.user
	try:
		asignacion=AsignacionParroquia.objects.get(persona__user=usuario,
			periodoasignacionparroquia__estado=True)
	except ObjectDoesNotExist:
		raise PermissionDenied

	p=ParametrizaParroquia.objects.filter(parroquia=asignacion.parroquia)
	of=''
	for o in p:
		of=o
	if p:
		if request.method == 'POST':
			form_parametriza = ParametrizaParroquiaForm(usuario,request.POST, instance=of)
			if form_parametriza.is_valid():
				form_parametriza.save()
				LogEntry.objects.log_action(
	            	user_id=request.user.id,
	            	content_type_id=ContentType.objects.get_for_model(of).pk,
	            	object_id=of.id,
	            	object_repr=unicode(of),
	            	action_flag=CHANGE,
	            	change_message="Parametriza Parroquia actualizada")
				
				return HttpResponseRedirect('/home/')
			else:
				ctx = {'form_parametriza':form_parametriza}
				messages.error(request,'Los datos del formulario son incorrectos')
				return render(request, 'parametriza/parroquia/parametriza_form.html', ctx)
		else:
			form_parametriza = ParametrizaParroquiaForm(usuario,instance=of)
			ctx = {'form_parametriza': form_parametriza, 'object':of}
			return render(request, 'parametriza/parroquia/parametriza_form.html', ctx)
	else:

		if(request.method=='POST'):
			form_parametriza=ParametrizaParroquiaForm(usuario,request.POST)
			
			if form_parametriza.is_valid():
				parametriza=form_parametriza.save(commit=False)
				parametriza.save()
				LogEntry.objects.log_action(
					user_id=request.user.id,
					content_type_id=ContentType.objects.get_for_model(parametriza).pk,
					object_id=parametriza.id,
					object_repr=unicode(parametriza),
					action_flag=ADDITION,
					change_message="Creo una parametriza parroquia"
					)
				return HttpResponseRedirect('/home/')
			else:
				ctx={'form_parametriza':form_parametriza}
				messages.error(request,'Los datos del formulario son incorrectos')
				return render(request,'parametriza/parroquia/parametriza_form.html',ctx)
		else:
			form_parametriza = ParametrizaParroquiaForm(usuario)
			ctx = {'form_parametriza': form_parametriza}
			return render(request, 'parametriza/parroquia/parametriza_form.html', ctx)


# views para los LOGS del ekklesia

class LogListView(ListView):
	model=LogEntry
	template_name='log/log_list.html'

	def get_queryset(self):
		try:
			if not (self.request.user.is_superuser):

				queryset = LogEntry.objects.all()
				return queryset
			

		except: 
			return [];
	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('admin.change_logentry', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(LogListView, self).dispatch(*args, **kwargs)
	

# TODOS LOS REPORTES


def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

@login_required(login_url='/login/')
def libro_pdf(request, pk):
	libro=get_object_or_404(Libro, pk=pk)
	html = render_to_string('libro/libro.html', {'pagesize':'A4', 'libro':libro}, 
		context_instance=RequestContext(request))
	return generar_pdf(html)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_matrimonio', login_url='/login/', 
	raise_exception=permission_required)
def matrimonio_certificado(request, pk):
	matrimonio=get_object_or_404(Matrimonio, pk=pk)
	try:
		asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
			periodoasignacionparroquia__estado=True)
		p=ParametrizaDiocesis.objects.all()

	except ObjectDoesNotExist:
		raise PermissionDenied
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
	notas=NotaMarginal.objects.filter(matrimonio=matrimonio)
	html = render_to_string('matrimonio/matrimonio_certificado.html', {'pagesize':'A4', 
		'matrimonio':matrimonio,'cura':cura,'notas':notas,'asignacion':asignacion,'p':p},
		context_instance=RequestContext(request))
	return generar_pdf(html)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_bautismo', login_url='/login/', 
	raise_exception=permission_required)
def bautismo_certificado(request, pk):
	bautismo=get_object_or_404(Bautismo, pk=pk)
	try:
		asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
			periodoasignacionparroquia__estado=True)
		p=ParametrizaDiocesis.objects.all()
	except ObjectDoesNotExist:
		raise PermissionDenied
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
			parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	html = render_to_string('bautismo/bautismo_certificado.html', {'pagesize':'A4', 'bautismo':bautismo,
		'cura':cura,'notas':notas,'asignacion':asignacion,'p':p},context_instance=RequestContext(request))
	return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_bautismo', login_url='/login/', 
	raise_exception=permission_required)
def bautismo_acta(request, pk):
	bautismo=get_object_or_404(Bautismo, pk=pk)
	try:
		asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
			periodoasignacionparroquia__estado=True)
		p=ParametrizaDiocesis.objects.all()
	except ObjectDoesNotExist:
		raise PermissionDenied
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
	notas=NotaMarginal.objects.filter(bautismo=bautismo)
	html = render_to_string('bautismo/bautismo_acta.html', {'pagesize':'A4', 'bautismo':bautismo,
		'cura':cura,'notas':notas,'asignacion':asignacion,'p':p},context_instance=RequestContext(request))
	return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_confirmacion', login_url='/login/', 
	raise_exception=permission_required)
def confirmacion_reporte(request, pk):
	confirmacion=get_object_or_404(Confirmacion, pk=pk)
	try:
		asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
			periodoasignacionparroquia__estado=True)
		p=ParametrizaDiocesis.objects.all()
		
	except ObjectDoesNotExist:
		raise PermissionDenied
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
	html = render_to_string('confirmacion/confirmacion_certificado.html', 
		{'pagesize':'A4', 'confirmacion':confirmacion,'cura':cura,'asignacion':asignacion,'p':p},
		context_instance=RequestContext(request))
	return generar_pdf(html)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_eucaristia', login_url='/login/', 
	raise_exception=permission_required)
def eucaristia_reporte(request, pk):
	eucaristia=get_object_or_404(Eucaristia, pk=pk)
	try:
		asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
			periodoasignacionparroquia__estado=True)
		p=ParametrizaDiocesis.objects.all()
	except ObjectDoesNotExist:
		raise PermissionDenied
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
	# notas=NotaMarginal.objects.filter()
	html = render_to_string('eucaristia/eucaristia_certificado.html', {'pagesize':'A4', 'eucaristia':eucaristia,
		'cura':cura,'asignacion':asignacion,'p':p},context_instance=RequestContext(request))
	return generar_pdf(html)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_feligres', login_url='/login/', 
	raise_exception=permission_required)
def usuario_reporte_honorabilidad(request,pk):
	perfil=get_object_or_404(PerfilUsuario,pk=pk)
	# parroquia=AsignacionParroquia.objects.get(persona__user=request.user).parroquia
	try:
		asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
			periodoasignacionparroquia__estado=True)
		p=ParametrizaDiocesis.objects.all()
	except ObjectDoesNotExist:
		raise PermissionDenied
	cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
		parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
	html = render_to_string('usuario/certificado_honorabilidad.html', {'pagesize':'A4', 'perfil':perfil,
		'cura':cura,'asignacion':asignacion,'p':p},context_instance=RequestContext(request))
	return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_matrimonio', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_bautismo', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_eucaristia', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_confirmacion', login_url='/login/', 
	raise_exception=permission_required)
def reporte_anual_sacramentos(request):
	anio_actual=request.GET.get('anio')
	# print("El año ingresado es: %d"%anio_actual)
	template_name = "reportes/reporte_anual_sacramentos_form.html"
	if anio_actual== anio_actual:

		if anio_actual:
			ninios1=0
			ninios7=0
			ninios=0
			try:
				asignacion= AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			bautismos=Bautismo.objects.filter(fecha_sacramento__year=anio_actual,
				parroquia=asignacion.parroquia)
			num_bautizos=len(bautismos)
			for b in bautismos:
				print("Bautismos en 2013 son: %s" %(len(bautismos)))
				num_bautizos=len(bautismos)
				anios_bautizados=b.bautizado.fecha_nacimiento.year
				# print('años de los bautizados en año:%d son: %d' %(int(anio_actual),bautizados))
				resta=int(anio_actual)-anios_bautizados
				if(resta<=1):
					ninios1=ninios1+1
					print ("Niños hasta 1 año %s"%ninios1)
				elif(resta>1 and resta<=7):
					ninios7=ninios7+1
					print('Niños de 1 a 7: %s' %ninios7)
				else:
					ninios=ninios+1
					print('Niños mayores de 7: %s' % ninios)

			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			# bautismos=Bautismo.objects.filter(fecha_sacramento__year=anio_actual).count()
			eucaristias=Eucaristia.objects.filter(fecha_sacramento__year=anio_actual,
				parroquia=asignacion.parroquia).count()
			confirmaciones=Confirmacion.objects.filter(fecha_sacramento__year=anio_actual,
				parroquia=asignacion.parroquia).count()
			catolicos=Matrimonio.objects.filter(fecha_sacramento__year=anio_actual,
				tipo_matrimonio='Catolico',parroquia=asignacion.parroquia).count()
			mixtos=Matrimonio.objects.filter(fecha_sacramento__year=anio_actual,tipo_matrimonio='Mixto',
				parroquia=asignacion.parroquia).count()
			matrimonios=catolicos+mixtos
			form = ReporteSacramentosAnualForm(request.GET)
			if(bautismos or eucaristias or confirmaciones or matrimonios):
				if form.is_valid():
					html=render_to_string('reportes/reporte_anual_sacramentos.html',
					{'pagesize':'A4','num_bautizos':num_bautizos,'ninios1':ninios1,'ninios7':ninios7,
					'ninios':ninios,'eucaristias':eucaristias,'confirmaciones':confirmaciones,
					'catolicos':catolicos,'mixtos':mixtos,'asignacion':asignacion,'cura':cura,
					'anio_actual':anio_actual,'matrimonios':matrimonios,'p':p},
					context_instance=RequestContext(request))
					return generar_pdf(html)
					
					
				else:
					messages.error(request, 'Los datos del formulario son incorrectos')
					ctx = {'form': form}
					# return render(request, template_name, ctx)
			else:
				messages.error(request,'No hay sacramentos en este año')
				ctx={'form':form}
		else:
			form = ReporteSacramentosAnualForm()
	else:
		messages.error(request, 'El año tiene que ser de 4 digitos')
		ctx = {'form': form}


		
	ctx={'form':form}
	return render(request, template_name, ctx)

	
@login_required(login_url='/login/')
@permission_required('sacramentos.add_intenciones', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_intenciones', login_url='/login/', 
	raise_exception=permission_required)
def reporte_intenciones(request):
	tipo=request.GET.get('tipo')
	fecha=request.GET.get('fecha')
	# mes=request.GET.get('fecha')
	hora=request.GET.get('hora')
	template_name = "reportes/reporte_intenciones_form.html"
	if tipo=='d':
		if fecha and not hora:
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			
			intenciones=Intenciones.objects.filter(fecha=fecha,
				parroquia=asignacion.parroquia).order_by('hora')
			suma=Intenciones.objects.filter(fecha=fecha,
				parroquia=asignacion.parroquia).aggregate(Sum('ofrenda'))['ofrenda__sum']
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			form = ReporteIntencionesForm(request.GET)
			if (intenciones):
				
				if form.is_valid():
					html=render_to_string('reportes/reporte_intenciones.html',
					{'pagesize':'A4','intenciones':intenciones,'asignacion':asignacion,
					'cura':cura,'suma':suma,'p':p},
					context_instance=RequestContext(request))
					return generar_pdf(html)
				
				
				else:
					messages.error(request, 'Los datos del formulario son incorrectos')
					ctx = {'form': form}
					return render(request, template_name, ctx)
			else:
				messages.error(request,'No hay intenciones en ha fecha ingresada')
				ctx={'form':form}
				return render(request, template_name, ctx)

		if fecha and hora:
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			intenciones=Intenciones.objects.filter(fecha=fecha,hora=hora,
				parroquia=asignacion.parroquia).order_by('hora')
			suma=Intenciones.objects.filter(fecha=fecha,hora=hora,
				parroquia=asignacion.parroquia).aggregate(Sum('ofrenda'))['ofrenda__sum']
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			form = ReporteIntencionesForm(request.GET)
			if(intenciones):

				if form.is_valid():
					html=render_to_string('reportes/reporte_intenciones.html',
					{'pagesize':'A4','intenciones':intenciones,'asignacion':asignacion,
					'cura':cura,'suma':suma,'p':p},
					context_instance=RequestContext(request))
					return generar_pdf(html)
				
				
				else:
					messages.error(request, 'Los datos del formulario son incorrectos')
					ctx = {'form': form}
					return render(request, template_name, ctx)
			else:
				messages.error(request,'No hay intenciones en ha fecha ingresada')
				ctx={'form':form}
				return render(request, template_name, ctx)

	if tipo=='m':
		
		if fecha :
			mes=fecha[5:7]
			anio=fecha[:4]
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			intenciones=Intenciones.objects.filter(fecha__year=anio,fecha__month=mes,
				parroquia=asignacion.parroquia).order_by('hora')
			suma=Intenciones.objects.filter(fecha__year=anio,fecha__month=mes,
				parroquia=asignacion.parroquia).aggregate(Sum('ofrenda'))['ofrenda__sum']
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			form = ReporteIntencionesForm(request.GET)
			if(intenciones):
				if form.is_valid():
					html=render_to_string('reportes/reporte_intenciones.html',
					{'pagesize':'A4','intenciones':intenciones,'asignacion':asignacion,
					'cura':cura,'suma':suma,'p':p},
					context_instance=RequestContext(request))
					return generar_pdf(html)
					
				else:
					messages.error(request, 'Los datos del formulario son incorrectos')
					ctx = {'form': form}
					return render(request, template_name, ctx)
			else:
				messages.error(request,'No hay intenciones en ha fecha ingresada')
				ctx={'form':form}
				return render(request, template_name, ctx)

	if tipo=='a':
		if fecha:
			fecha=fecha
			anio=fecha[:4]
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			intenciones=Intenciones.objects.filter(fecha__year=anio,
				parroquia=asignacion.parroquia).order_by('hora')
			suma=Intenciones.objects.filter(fecha__year=anio,
				parroquia=asignacion.parroquia).aggregate(Sum('ofrenda'))['ofrenda__sum']
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			form = ReporteIntencionesForm(request.GET)
			if(intenciones):
				if form.is_valid():
					html=render_to_string('reportes/reporte_intenciones.html',
					{'pagesize':'A4','intenciones':intenciones,'asignacion':asignacion,
					'cura':cura,'suma':suma,'p':p},
					context_instance=RequestContext(request))
					return generar_pdf(html)
				
				
				else:
					messages.error(request, 'Los datos del formulario son incorrectos')
					ctx = {'form': form}
					return render(request, template_name, ctx)
			else:
				messages.error(request,'No hay intenciones en la fecha ingresada')
				ctx = {'form': form}
				return render(request, template_name, ctx)
	else:
		form = ReporteIntencionesForm()
				
	ctx={'form':form}
	return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_bautismo', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_matrimonio', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_eucaristia', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_confirmacion', login_url='/login/', 
	raise_exception=permission_required)
@permission_required('sacramentos.change_feligres', login_url='/login/', 
	raise_exception=permission_required)
def reporte_permisos(request):
	template_name = "reportes/reporte_permiso_form.html"
	if request.method=='POST':
		feligres=request.POST.get('feligres')
		tipo=request.POST.get('tipo')
		form=ReportePermisoForm(request.POST)
		if (tipo =='Bautismo' and feligres):
			
			feligres=PerfilUsuario.objects.get(pk=feligres)
			print(feligres)
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			try:
				if Bautismo.objects.get(bautizado=feligres):
					messages.error(request,'El feligres tiene registrado un Bautismo')
					queryset=PerfilUsuario.objects.filter(pk=feligres.pk)
					form=ReportePermisoForm(queryset,request.POST)
					ctx={'form':form}
					return render(request, template_name, ctx)
			except ObjectDoesNotExist:
				html=render_to_string('reportes/reporte_permiso.html',
					{'pagesize':'A4','feligres':feligres,'asignacion':asignacion,'cura':cura,
					'tipo':tipo,'p':p},context_instance=RequestContext(request))
				return generar_pdf(html)
			
			
		elif (tipo =='Eucaristia' and feligres):
			
			feligres=PerfilUsuario.objects.get(id=feligres)
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			
			try:
				if Eucaristia.objects.get(feligres=feligres):
					messages.error(request,'El feligres tiene registrado una Eucaristia')
					queryset=PerfilUsuario.objects.filter(pk=feligres.pk)
					form=ReportePermisoForm(queryset,request.POST)
					ctx={'form':form}
					return render(request, template_name, ctx)
			except ObjectDoesNotExist:
				html=render_to_string('reportes/reporte_permiso.html',
				{'pagesize':'A4','feligres':feligres,'asignacion':asignacion,'cura':cura,
				'tipo':tipo,'p':p},
				context_instance=RequestContext(request))
				return generar_pdf(html)
				
			
		elif (tipo =='Confirmacion' and feligres):
			
			feligres=PerfilUsuario.objects.get(id=feligres)
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			try:
				if Confirmacion.objects.get(confirmado=feligres):
					messages.error(request,'El feligres tiene registrado una Confirmacion')
					queryset=PerfilUsuario.objects.filter(pk=feligres.pk)
					form=ReportePermisoForm(queryset,request.POST)
					ctx={'form':form}
					return render(request, template_name, ctx)
			except ObjectDoesNotExist:
				html=render_to_string('reportes/reporte_permiso.html',
					{'pagesize':'A4','feligres':feligres,'asignacion':asignacion,'cura':cura,
					'tipo':tipo,'p':p},
					context_instance=RequestContext(request))
				return generar_pdf(html)
			

		elif tipo =='Matrimonio' and feligres:
			
			feligres=PerfilUsuario.objects.get(id=feligres)
			try:
				asignacion=AsignacionParroquia.objects.get(persona__user=request.user,
					periodoasignacionparroquia__estado=True)
				p=ParametrizaDiocesis.objects.all()
			except ObjectDoesNotExist:
				raise PermissionDenied
			cura=AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
				parroquia=asignacion.parroquia,periodoasignacionparroquia__estado=True)
			
			if feligres.sexo=='m':
				if Matrimonio.objects.filter(novio=feligres,vigente=True):
					messages.error(request,'El feligres tiene registrado un matrimonio vigente')
					queryset=PerfilUsuario.objects.filter(pk=feligres.pk)
					form=ReportePermisoForm(queryset,request.POST)
					ctx={'form':form}
					return render(request, template_name, ctx)

				else:
					html=render_to_string('reportes/reporte_permiso.html',
						{'pagesize':'A4','feligres':feligres,'asignacion':asignacion,'cura':cura,
						'tipo':tipo,'p':p},context_instance=RequestContext(request))
					return generar_pdf(html)
			else:
				if Matrimonio.objects.filter(novia=feligres,vigente=True):
					messages.error(request,'El feligres tiene registrado un matrimonio vigente')
					queryset=PerfilUsuario.objects.filter(pk=feligres.pk)
					form=ReportePermisoForm(queryset,request.POST)
					ctx={'form':form}
					return render(request, template_name, ctx)
				else:
					html=render_to_string('reportes/reporte_permiso.html',
						{'pagesize':'A4','feligres':feligres,'asignacion':asignacion,'cura':cura,
						'tipo':tipo,'p':p},context_instance=RequestContext(request))
					return generar_pdf(html)

	else:
		form = ReportePermisoForm()
		ctx={'form':form}
		return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_parroquia', login_url='/login/', 
	raise_exception=permission_required)
def reporte_parroquias_sacerdotes(request,pk):
	persona=User.objects.get(pk=request.user.pk)
	parroquia=get_object_or_404(Parroquia, pk=pk)
	
	periodos=PeriodoAsignacionParroquia.objects.filter(asignacion__parroquia=parroquia,
		asignacion__persona__user__groups__name='Sacerdote')
	try:
		p=ParametrizaDiocesis.objects.all()
	except ObjectDoesNotExist:
		raise PermissionDenied

	print(periodos)
	html = render_to_string('reportes/reporte_parroquia_sacerdote.html', {'pagesize':'A4',
		'parroquia':parroquia,'periodos':periodos,'persona':persona,'p':p},
		context_instance=RequestContext(request))
	return generar_pdf(html)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_sacerdote', login_url='/login/', 
	raise_exception=permission_required)
def reporte_sacerdotes_parroquias(request,pk):
	persona=User.objects.get(pk=request.user.pk)
	cura=get_object_or_404(PerfilUsuario, pk=pk)
	periodos=PeriodoAsignacionParroquia.objects.filter(asignacion__persona=cura)
	p=ParametrizaDiocesis.objects.all()
	print(periodos)
	html = render_to_string('reportes/reporte_sacerdote_parroquia.html', {'pagesize':'A4',
		'periodos':periodos,'persona':persona,'cura':cura,'p':p},
		context_instance=RequestContext(request))
	return generar_pdf(html)


# exportar a csv los logs

@login_required(login_url='/login/')
@permission_required('admin.change_logentry', login_url='/login/', 
	raise_exception=permission_required)
def exportar_csv_logs(request):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename="logs.csv"'
    writer = csv.writer(response)
    logs = LogEntry.objects.all()
    writer.writerow(['id','action_time','user_id','content_type','object_id','object_repr','action_flag','change_message']) 
    for log in logs:
    	writer.writerow([log.id,log.action_time,log.user,log.content_type,log.object_id,encode(log.object_repr),log.action_flag,encode(log.change_message)])
    return response

# para poder exportar a csv con utf-8

def encode(text):
	return text.encode('utf-8')


