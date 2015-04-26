# -*- coding:utf-8 -*-
# Create your views here.
import json
from smtplib import SMTPAuthenticationError
import unicodedata
import logging
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .forms import SendEmailForm, GruposForm
from sacramentos.models import PeriodoAsignacionParroquia, AsignacionParroquia
from core.views import BusquedaMixin
from core.constants import *

logger = logging.getLogger(__name__)

# Login con AthenticateForm
def login_view(request):
    redirect_to = request.REQUEST.get('next', '')
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        form.fields["username"].widget = forms.TextInput(attrs={'required': '', 'maxlength': 25})
        form.fields["password"].widget = forms.TextInput(attrs={'required': '', 'type': 'password', 'maxlength': 25})

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            print user.backend
            print type(user)

            if user is not None and user.is_active:

                try:
                    parroquia = AsignacionParroquia.objects.get(persona__user=user, es_activo=True).parroquia
                    if parroquia:
                        request.session["parroquia"] = parroquia
                        logger.error("Entré al login")
                        logger.info("parroquia: %s" % parroquia)
                        print 'Entré al login'
                        print parroquia
                        login(request, user)
                except ObjectDoesNotExist:
                    administrador = Group.objects.get(name='Administrador')
                    if administrador in user.groups.all():
                        login(request, user)
                    else:
                        messages.add_message(request, messages.ERROR, 'Ud. no tiene una asignación activa en la Parroquia')
                        ctx = {'form': form}
                        return render(request, 'login.html', locals())

                except MultipleObjectsReturned:
                    return HttpResponseRedirect('/seleccionar/parroquia/%s' % user.id)

                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.add_message(request, messages.ERROR, 'Ud. no tiene permisos para acceder al sistema')
                ctx = {'form': form}
                return render(request, 'login.html', locals())
        else:
            messages.add_message(request, messages.ERROR, '%s' % form.errors.get('__all__')[0])
            ctx = {'form': form}
            return render(request, 'login.html', locals())
    else:
        form = AuthenticationForm()
        form.fields["username"].widget = forms.TextInput(attrs={'required': '', 'maxlength': 25})
        form.fields["password"].widget = forms.TextInput(attrs={'required': '', 'type': 'password', 'maxlength': 25})
    ctx = {'form': form}
    return render(request, 'login.html', locals())


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


# Cambiar la contraseña sin proporcionar la antigua contraseña
@login_required(login_url='/login/')
def change_password_view(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.add_message(request, messages.INFO, 'El cambio de clave se realizó con éxito')
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.ERROR, MENSAJE_ERROR)
    else:
        form = SetPasswordForm(user)

    ctx = {'form': form}
    return render(request, 'change-password.html', ctx)


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
            messages.add_message(request, messages.ERROR, MENSAJE_ERROR)
    else:
        form = PasswordChangeForm(user)

    ctx = {'form': form}
    return render(request, 'change-password.html', ctx)


def send_email_view(request):
    template_name = 'send_password.html'
    success_url = '/login/'
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        form.fields["email"].widget = forms.TextInput(attrs={'required': ''})
        if form.is_valid():
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            nuevo_password = User.objects.make_random_password(length=8,
                                                               allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            user.set_password(nuevo_password)
            user.save()
            subject, from_email, to = 'Recuperación de la contraseña', 'from@server.com', email
            text_content = u'Su nueva contraseña es: %s Cámbiela por una que ud recuerde fácilmente' % nuevo_password
            html_content = u'<p>Su nueva contraseña es:  <strong> %s </strong></p><p>Cámbiela por una que ud recuerde fácilmente</p>' % nuevo_password
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")

            try:
                msg.send()
            except SMTPAuthenticationError:
                messages.add_message(request, messages.ERROR, MENSAJE_ERROR_CORREO)
                logger.error('Las credenciales del correo de soporte técnico son incorrectas')

            return HttpResponseRedirect(success_url)

        else:
            ctx = {'form': form}
            return render(request, template_name, ctx)
    else:
        form = SendEmailForm()
        form.fields["email"].widget = forms.TextInput(attrs={'required': ''})
        ctx = {'form': form}
        return render(request, template_name, ctx)


class GroupCreate(CreateView):
    model = Group
    success_url = reverse_lazy('group_list')
    form_class = GruposForm

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('auth.add_group', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(GroupCreate, self).dispatch(*args, **kwargs)


class GroupUpdate(UpdateView):
    """docstring for GroupUpdate"""
    model = Group
    template_name = 'auth/group_form.html'
    context_object_name = 'form'
    success_url = reverse_lazy('group_list')
    form_class = GruposForm

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('auth.change_group', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(GroupUpdate, self).dispatch(*args, **kwargs)


class GroupList(BusquedaMixin, ListView):
    model = Group
    context_object_name = 'object_list'
    template_name = 'auth/group_list.html'
    paginate_by = 10

    @method_decorator(login_required(login_url='login'))
    @method_decorator(permission_required('auth.change_group', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(GroupList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        name = self.request.GET.get('q', '')
        if (name != ''):
            name = ''.join((c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
            return Group.objects.filter(name__icontains=name).order_by('name')
        else:
            return Group.objects.all().order_by('name')
