# -*- coding:utf-8 -*-
# Create your views here.
import json
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .forms import SendEmailForm, GruposForm
from sacramentos.models import PeriodoAsignacionParroquia

#Login de usuarios sin utilizar ningún formulario preestablecido
# def login_view(request):
# 	if request.user.is_authenticated():
# 		return HttpResponseRedirect('/feligres/add')
# 	else:
# 		if request.method == 'POST':
# 			username = request.POST['username']
# 			password = request.POST['password']
# 			user = authenticate(username=username, password=password)
# 			if user is not None and user.is_active:
# 				login(request,user)
# 				return HttpResponseRedirect('/')
# 			else:
# 				messages.add_message(request, messages.ERROR, 'El user o la pass son incorrectas')
# 		return render(request, 'login.html')


#Login con AthenticateForm	
def login_view(request):
	redirect_to = request.REQUEST.get('next', '')
	if request.user.is_authenticated():
		return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
	if request.method == 'POST':		
		form = AuthenticationForm(data=request.POST)
		form.fields["username"].widget = forms.TextInput(attrs={'required':'', 'maxlength':20})
		form.fields["password"].widget = forms.TextInput(attrs={'required':'','type':'password', 'maxlength':20})

		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			print 'imprimiendo meta: %s' %redirect_to
			if user is not None and user.is_active and user.is_staff:
				login(request, user)
				try:
					parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user, estado=True).asignacion.parroquia
					if parroquia:
						request.session["parroquia"] = parroquia
				except ObjectDoesNotExist:
					pass
				if redirect_to:
					return HttpResponseRedirect(redirect_to)
				else:
					return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
			else:
				messages.add_message(request, messages.ERROR, 'Ud. no tiene permisos para acceder al sistema')
		else:
			messages.add_message(request, messages.ERROR, 'El nombre de usuario o la contraseña están incorrectos')
	else:
		form = AuthenticationForm()
		form.fields["username"].widget = forms.TextInput(attrs={'required':'', 'maxlength':25})
		form.fields["password"].widget = forms.TextInput(attrs={'required':'','type':'password', 'maxlength':20})
	ctx =  {'form':form}
	return render(request, 'login.html',locals())

@login_required(login_url='/login/')
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

##Cambiar la contraseña sin proporcionar la antigua contraseña
# @login_required(login_url='/login/')
# def change_password_view(request):
# 	user = request.user
# 	if request.method == 'POST':
# 		form = SetPasswordForm(user, request.POST)
# 		if form.is_valid():
# 			form.save()
# 			logout(request)
# 			messages.add_message(request, messages.INFO, 'El cambio de clave se realizó con éxito')
# 			return HttpResponseRedirect('/')
# 		else:
# 			messages.add_message(request, messages.ERROR, 'Los datos ingresados no son válidos')
# 	else:
# 		form = SetPasswordForm(user)

# 	ctx = {'form': form}
# 	return render(request, 'change-password.html', ctx)
# 	

#Cambiar la contraseña proporcionando la antigua contraseña 
@login_required(login_url='/login/')
def change_password_view(request):
	user = request.user
	if request.method == 'POST':
		form = PasswordChangeForm(user, request.POST)
		if form.is_valid():
			form.save()
			logout(request)
			messages.add_message(request, messages.INFO, 'El cambio de clave se realizó con éxito')
			return HttpResponseRedirect('/')
		else:
			messages.add_message(request, messages.ERROR, 'Revise los errores')
	else:
		form = PasswordChangeForm(user)

	ctx = {'form': form}
	return render(request, 'change-password.html', ctx)

def send_email_view(request):
	template_name = 'send_password.html' 
	success_url = '/login/'
	if request.method == 'POST':
		form = SendEmailForm(request.POST)
		form.fields["email"].widget = forms.TextInput(attrs={'required':''})
		if form.is_valid():
			email = request.POST.get('email')
			user = User.objects.get(email=email)
			nuevo_password = User.objects.make_random_password(length=8, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789') 
			user.set_password(nuevo_password)
			user.save()
			subject, from_email, to = 'Recuperación de la contraseña', 'from@server.com', email
			text_content = u'Su nueva contraseña es: %s Cámbiela por una que ud recuerde fácilmente' % nuevo_password
			html_content = u'<p>Su nueva contraseña es:  <strong> %s </strong></p><p>Cámbiela por una que ud recuerde fácilmente</p>' % nuevo_password
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			return HttpResponseRedirect(success_url)
		
		else:
			ctx = {'form': form}
			return render(request, template_name, ctx)
	else:
		form = SendEmailForm()
		form.fields["email"].widget = forms.TextInput(attrs={'required':''})
		ctx = {'form': form}
		return render(request, template_name, ctx)


	

class GroupCreate(CreateView):
	model = Group
	success_url = '/group/'
	form_class = GruposForm

	@method_decorator(login_required(login_url='login'))
	@method_decorator(permission_required('auth.add_group', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(GroupCreate, self).dispatch(*args, **kwargs)


class GroupUpdate(UpdateView):
	"""docstring for GroupUpdate"""
	model = Group
	template_name       = 'auth/group_form.html'
	context_object_name = 'form'
	success_url = '/group/'
	form_class = GruposForm

	@method_decorator(login_required(login_url='login'))
	@method_decorator(permission_required('auth.change_group', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(GroupUpdate, self).dispatch(*args, **kwargs)

class GroupList(ListView):
	model = Group
	context_object_name = 'object_list'
	template_name = 'auth/group_list.html'

	@method_decorator(login_required(login_url='login'))
	@method_decorator(permission_required('auth.change_group', login_url='/login/',
		raise_exception=permission_required))
	def dispatch(self, *args, **kwargs):
		return super(GroupList, self).dispatch(*args, **kwargs)

	
		

	
		

