# -*- coding: utf-8 -*-
import json
import logging

from django.shortcuts import render_to_response,render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .forms	import ProvinciaForm,CantonForm,ParroquiaForm
from .models import Provincia,Canton,Parroquia

logger = logging.getLogger(__name__)

#Vistas para la clase Parroquia

class ProvinciaList(ListView):
	model                 = Provincia 
	template_name         = 'provincia/provincia_list.html'
	# context_object_name = 'list_parroquia'
	# paginate_by = 5

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.change_provincia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ProvinciaList, self).dispatch(*args, **kwargs)

class ProvinciaCreate(CreateView):
	model               = Provincia
	template_name       = 'provincia/provincia_form.html'
	# context_object_name = 'form'
	success_url         = '/ciudades/provincia/'
	form_class = ProvinciaForm
	
	def form_invalid(self, form):
		messages.add_message(self.request, messages.ERROR, 'Datos incorrectos')
		return super(ProvinciaCreate, self).form_invalid(form)

	def form_valid(self, form):
		messages.add_message(self.request, messages.SUCCESS, 'Guardado exitosamente')
		return super(ProvinciaCreate, self).form_valid(form)
	
	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.add_provincia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ProvinciaCreate, self).dispatch(*args, **kwargs)


class ProvinciaUpdate(UpdateView):
	model               = Provincia 
	template_name       = 'provincia/provincia_form.html'
	context_object_name = 'form'
	success_url         = '/ciudades/provincia/'
	form_class = ProvinciaForm
	
	

	def form_valid(self, form):
		messages.add_message(self.request, messages.SUCCESS, 'Actualizado Exitosamente')
		return super(ProvinciaUpdate, self).form_valid(form)

	def form_invalid(self, form):
		messages.add_message(self.request, messages.ERROR, 'Uno o más datos son incorrectos')
		return super(ProvinciaUpdate, self).form_invalid(form)

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.change_provincia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ProvinciaUpdate, self).dispatch(*args, **kwargs)



class ProvinciaDelete(DeleteView):
	
	model         = Provincia
	template_name = 'provincia/provincia_confirm_delete.html'
	success_url   =  reverse_lazy('provincia_list')

	def delete(self, request, *args, **kwargs):
		messages.add_message(self.request, messages.ERROR, 'Eliminado Correctamente')
		return super(ProvinciaDelete, self).delete(request, *args, **kwargs)

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.delete_provincia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ProvinciaDelete, self).dispatch(*args, **kwargs)


class CantonList(ListView):
	model                 = Canton 
	template_name         = 'canton/canton_list.html'
	
	

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.change_canton', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(CantonList, self).dispatch(*args, **kwargs)


class CantonCreate(CreateView):
	model               = Canton
	template_name       = 'canton/canton_form.html'
	context_object_name = 'form'
	success_url         = '/ciudades/canton/'
	form_class = CantonForm
	
	def form_invalid(self, form):
		messages.add_message(self.request, messages.ERROR, 'Datos incorrectos')
		return super(CantonCreate, self).form_invalid(form)

	def form_valid(self, form):
		messages.add_message(self.request, messages.SUCCESS, 'Guardado exitosamente')
		return super(CantonCreate, self).form_valid(form)
	
	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.add_canton', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(CantonCreate, self).dispatch(*args, **kwargs)


class CantonUpdate(UpdateView):
	model               = Canton 
	template_name       = 'canton/canton_form.html'
	context_object_name = 'form'
	success_url         = '/ciudades/canton/'
	form_class = CantonForm
	

	def form_valid(self, form):
		messages.add_message(self.request, messages.WARNING, 'Objeto Actualizado')
		return super(CantonUpdate, self).form_valid(form)

	def form_invalid(self, form):
		messages.add_message(self.request, messages.ERROR, 'Datos incorrectos')
		return super(CantonUpdate, self).form_invalid(form)

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.change_canton', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(CantonUpdate, self).dispatch(*args, **kwargs)



class CantonDelete(DeleteView):
	
	model         = Canton
	template_name = 'canton/canton_confirm_delete.html'
	success_url   =  reverse_lazy('canton_list')

	def delete(self, request, *args, **kwargs):
		messages.add_message(self.request, messages.ERROR, 'Eliminado Correctamente')
		return super(CantonDelete, self).delete(request, *args, **kwargs)

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.delete_canton', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(CantonDelete, self).dispatch(*args, **kwargs)


class ParroquiaList(ListView):
	model                 = Parroquia 
	template_name         = 'parroquiacivil/parroquia_list.html'
	# context_object_name = 'list_parroquia'
	# paginate_by = 5

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.change_parroquia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ParroquiaList, self).dispatch(*args, **kwargs)


class ParroquiaCreate(CreateView):
	model               = Parroquia
	template_name       = 'parroquiacivil/parroquia_form.html'
	context_object_name = 'form'
	success_url         = '/ciudades/parroquia/'
	form_class = ParroquiaForm
	
	def form_invalid(self, form):
		messages.add_message(self.request, messages.ERROR, 'Datos incorrectos')
		return super(ParroquiaCreate, self).form_invalid(form)

	def form_valid(self, form):
		messages.add_message(self.request, messages.SUCCESS, 'Guardado exitosamente')
		return super(ParroquiaCreate, self).form_valid(form)
	
	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.add_parroquia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ParroquiaCreate, self).dispatch(*args, **kwargs)


class ParroquiaUpdate(UpdateView):
	model               = Parroquia 
	template_name       = 'parroquiacivil/parroquia_form.html'
	context_object_name = 'form'
	success_url         = '/ciudades/parroquia/'
	form_class = ParroquiaForm

	def form_valid(self, form):
		messages.add_message(self.request, messages.WARNING, 'Objeto Actualizado')
		return super(ParroquiaUpdate, self).form_valid(form)

	def form_invalid(self, form):
		messages.add_message(self.request, messages.ERROR, 'Datos incorrectos')
		return super(ParroquiaUpdate, self).form_invalid(form)

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.change_parroquia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ParroquiaUpdate, self).dispatch(*args, **kwargs)


class ParroquiaDelete(DeleteView):
	
	model         = Parroquia
	template_name = 'parroquiacivil/parroquia_confirm_delete.html'
	success_url   =  reverse_lazy('parroquiacivil_list')

	def delete(self, request, *args, **kwargs):
		messages.add_message(self.request, messages.ERROR, 'Eliminado Correctamente')
		return super(ParroquiaDelete, self).delete(request, *args, **kwargs)

	@method_decorator(login_required(login_url='/login/'))
	@method_decorator(permission_required('ciudades.delete_parroquia', login_url='/login/', 
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(ParroquiaDelete, self).dispatch(*args, **kwargs)