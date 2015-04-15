# -*- coding:utf-8 -*-
import json
import csv
import unicodedata
from datetime import datetime
from datetime import date
from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sessions.models import Session
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.forms.util import ErrorList
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.html import format_html, mark_safe
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
# Para los logs
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

from xhtml2pdf import pisa
import StringIO
import cgi
import reportlab

from sacramentos.models import (PerfilUsuario,
                                Libro, Matrimonio, Bautismo, Eucaristia, Confirmacion, NotaMarginal,
                                Parroquia, Intencion,
                                AsignacionParroquia, PeriodoAsignacionParroquia,
                                ParametrizaDiocesis, ParametrizaParroquia,
                                Iglesia
                                )

from sacramentos.forms import (
UsuarioForm, UsuarioPadreForm, UsuarioSacerdoteForm, UsuarioAdministradorForm, UsuarioSecretariaForm,
PerfilUsuarioForm, PadreForm, SacerdoteForm, AdministradorForm, AdminForm, SecretariaForm,
EmailForm,
MatrimonioForm, MatrimonioForm,
BautismoForm,
EucaristiaForm, EucaristiaForm,
ConfirmacionForm, ConfirmacionForm,
LibroForm, LibroBaseForm, NotaMarginalForm,
DivErrorList,
IntencionForm,
ParroquiaForm,
IglesiaForm,
AsignarParroquiaForm, PeriodoAsignacionParroquiaForm,
AsignarSecretariaForm,
ParametrizaDiocesisForm, ParametrizaParroquiaForm,
ReporteIntencionesForm, ReporteSacramentosAnualForm, ReportePermisoForm,
)

from ciudades.forms import DireccionForm
from ciudades.models import Canton, Provincia, Parroquia as ParroquiaCivil
from core.views import BusquedaMixin, BusquedaPersonaMixin, PaginacionMixin
from core.constants import MENSAJE_ERROR, MENSAJE_EXITO_CREACION, MENSAJE_EXITO_ACTUALIZACION
from core.models import Item
_reportlab_version = tuple(map(int, reportlab.Version.split('.')))
if _reportlab_version < (2, 1):
    raise ImportError("Reportlab Version 2.1+ is needed!")

REPORTLAB22 = _reportlab_version >= (2, 2)


@login_required(login_url='/login/')
def configuracion_inicial_view(request):
    template_name = 'configuracion/configuracion_inicial.html'
    iglesia = Iglesia.objects.exists()
    bautismo = Libro.objects.filter(tipo_libro='bautismo', principal=True).exists()
    eucaristia = Libro.objects.filter(tipo_libro='eucaristia', principal=True).exists()
    confirmacion = Libro.objects.filter(tipo_libro='confirmacion', principal=True).exists()
    matrimonio = Libro.objects.filter(tipo_libro='matrimonio', principal=True).exists()
    ctx = {
    'iglesia': iglesia,
    'libro_bautismo': bautismo,
    'libro_eucaristia': eucaristia,
    'libro_confirmacion': confirmacion,
    'libro_matrimonio': matrimonio
    }
    return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_feligres', login_url='/login/', raise_exception=permission_required)
def usuarioCreateView(request):
    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST)
        form_perfil = PerfilUsuarioForm(request.POST)
        form_perfil.fields['padre'].queryset = PerfilUsuario.objects.male()
        form_perfil.fields['madre'].queryset = PerfilUsuario.objects.female()

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
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(reverse_lazy('usuario_list'))

        else:
            id_padre = request.POST.get('padre')
            id_madre = request.POST.get('madre')
            form_perfil = PerfilUsuarioForm(request.POST)

            if id_padre and id_madre:
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.filter(id=id_padre)
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.filter(id=id_madre)

            elif id_padre and not id_madre:
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.filter(id=id_padre)
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.none()

            elif not id_padre and id_madre:
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.none()
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.filter(id=id_madre)

            else:
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.none()
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.none()

            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil}
            return render(request, 'usuario/usuario_form.html', ctx)
    else:
        form_usuario = UsuarioForm()
        form_perfil = PerfilUsuarioForm()
        ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil}
        return render(request, 'usuario/usuario_form.html', ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_feligres', login_url='/login/',
                     raise_exception=permission_required)
def edit_usuario_view(request, pk):
    perfil = get_object_or_404(PerfilUsuario, pk=pk)
    user = perfil.user

    # if perfil.user.groups.filter(name='Administrador').exists() or perfil.user.groups.filter(name='Sacerdote').exists():
    # 	raise Http404

    if perfil.user.groups.filter(name='Sacerdote').exists():
        raise Http404

    if request.method == 'POST':
        form_usuario = UsuarioForm(request.POST, instance=user)
        form_perfil = PerfilUsuarioForm(request.POST, instance=perfil)
        form_perfil.fields['padre'].queryset = PerfilUsuario.objects.male()
        form_perfil.fields['madre'].queryset = PerfilUsuario.objects.female()

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
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect('/usuario')
        else:
            id_padre = request.POST.get('padre')
            id_madre = request.POST.get('madre')
            if id_padre and id_madre:
                form_perfil = PerfilUsuarioForm(request.POST, instance=perfil)
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.filter(pk=id_padre)
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.filter(pk=id_madre)
            elif id_padre and not id_madre:
                form_perfil = PerfilUsuarioForm(request.POST, instance=perfil)
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.filter(pk=id_padre)
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.none()
            elif not id_padre and id_madre:
                form_perfil = PerfilUsuarioForm(request.POST, instance=perfil)
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.filter(pk=id_madre)
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.none()
            else:
                form_perfil = PerfilUsuarioForm(request.POST, instance=perfil)
                form_perfil.fields['padre'].queryset = PerfilUsuario.objects.none()
                form_perfil.fields['madre'].queryset = PerfilUsuario.objects.none()

            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil, 'perfil': perfil}
            return render(request, 'usuario/usuario_form.html', ctx)

    else:
        form_perfil = PerfilUsuarioForm(instance=perfil)
        form_usuario = UsuarioForm(instance=user)

    ctx = {'form_usuario': form_usuario, 'form_perfil': form_perfil, 'perfil': perfil}
    return render(request, 'usuario/usuario_form.html', ctx)


class UsuarioListView(BusquedaPersonaMixin, ListView):
    model = PerfilUsuario
    template_name = "usuario/usuario_list.html"
    queryset = PerfilUsuario.objects.feligres()
    paginate_by = 10

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_feligres',
                                          login_url='/login/', raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioListView, self).dispatch(*args, **kwargs)


    def get_queryset(self):
        name = self.request.GET.get('q', '')
        if (name != ''):
            # name = ' '.join(name.split())
            name = ''.join((c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
            return PerfilUsuario.objects.feligres().filter(
                Q(nombres_completos__icontains=name) |
                Q(dni=name)).order_by('user__last_name')
        else:
            return PerfilUsuario.objects.feligres()


class UsuarioDetailView(DetailView):
    model = PerfilUsuario
    template_name = 'usuario/usuario_detail.html'


    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_feligres',
                                          login_url='/login/', raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioDetailView, self).dispatch(*args, **kwargs)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_administrador', login_url='/login/',
                     raise_exception=permission_required)
def administrator_create_view(request):
    template_name = 'usuario/admin_form.html'
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
                usuario.is_staff = True
            else:
                usuario.is_staff = False

            usuario.save()
            return HttpResponseRedirect(success_url)
        else:
            form_email = EmailForm()
            administrador = persona
            form.fields['administrador'].queryset = PerfilUsuario.objects.filter(pk=administrador.id)
            ctx = {'form': form, 'form_email': form_email, 'administrador': administrador}
            return render(request, template_name, ctx)
    else:
        form = AdminForm()
        ctx = {'form': form}
        return render(request, template_name, ctx)


def administrador_create_view(request):
    template_name = 'usuario/administrador_form.html'
    success_url = '/administrador/'

    if request.method == 'POST':
        form_perfil = AdministradorForm(request.POST)
        form_usuario = UsuarioAdministradorForm(request.POST)

        if form_perfil.is_valid() and form_usuario.is_valid():
            administrador, created = Group.objects.get_or_create(name='Administrador')
            usuario = form_usuario.save(commit=False)
            perfil = form_perfil.save(commit=False)
            usuario.username = perfil.crear_username(usuario.first_name, usuario.last_name)
            usuario.set_password(usuario.username)
            usuario.save()
            usuario.groups.add(administrador)
            perfil.user = usuario
            perfil.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(perfil).pk,
                object_id=perfil.id,
                object_repr=unicode(perfil),
                action_flag=ADDITION,
                change_message="Creo un administrador")
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(success_url)

        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_perfil': form_perfil, 'form_usuario': form_usuario}
            return render(request, template_name, ctx)

    else:
        form_perfil = AdministradorForm()
        form_usuario = UsuarioAdministradorForm()
        ctx = {'form_perfil': form_perfil, 'form_usuario': form_usuario}
        return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_administrador', login_url='/login/',
                     raise_exception=permission_required)
def administrador_update_view(request, pk):
    perfil = get_object_or_404(PerfilUsuario, pk=pk)
    template_name = 'usuario/administrador_form.html'
    success_url = '/administrador/'

    if request.method == 'POST':
        staff = request.POST.get('is_staff')
        form_perfil = AdministradorForm(request.POST, instance=perfil)
        form_usuario = UsuarioAdministradorForm(request.POST, instance=perfil.user)

        if request.user == perfil.user and not staff:
            form_usuario.errors["is_staff"] = ErrorList([u'No está permitido que Ud se desactive del sistema.'])

        if form_perfil.is_valid() and form_usuario.is_valid():
            usuario = form_usuario.save()
            perfil = form_perfil.save()
            if not usuario.is_staff:
                #Esta linea de código permite desloguear a un usuario de manera remota
                [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == usuario.id]
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(perfil).pk,
                object_id=perfil.id,
                object_repr=unicode(perfil),
                action_flag=CHANGE,
                change_message="Administrador actualizado")
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(success_url)

        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_perfil': form_perfil, 'form_usuario': form_usuario, 'object': perfil}
            return render(request, template_name, ctx)

    else:
        form_perfil = AdministradorForm(instance=perfil)
        form_usuario = UsuarioAdministradorForm(instance=perfil.user)
        ctx = {'form_perfil': form_perfil, 'form_usuario': form_usuario, 'object': perfil}
        return render(request, template_name, ctx)


class AdministradorListView(ListView):
    model = PerfilUsuario
    template_name = "usuario/administrador_list.html"
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('q', '')
        if (name != ''):
            # name = ' '.join(name.split())
            name = ''.join((c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
            return PerfilUsuario.objects.administrador().filter(
                Q(nombres_completos__icontains=name) |
                Q(dni=name)).order_by('user__last_name')
        else:
            return PerfilUsuario.objects.administrador().order_by('user__last_name')

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
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(success_url)
        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_usuario': usuario_form, 'form_perfil': perfil_form, 'object': secretaria}
            return render(request, template_name, ctx)
    else:
        perfil_form = SecretariaForm(instance=secretaria)
        usuario_form = UsuarioSecretariaForm(instance=secretaria.user)
        ctx = {'form_usuario': usuario_form, 'form_perfil': perfil_form, 'object': secretaria}
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
            usuario = form_usuario.save(commit=False)
            sacerdote = form_sacerdote.save(commit=False)
            usuario.username = sacerdote.crear_username(usuario.first_name, usuario.last_name)
            usuario.set_password(usuario.username)
            usuario.save()
            usuario.groups.add(sacerdotes)
            sacerdote.user = usuario
            sacerdote.sexo = Item.objects.masculino()
            sacerdote.profesion = 'Sacerdote'
            sacerdote.estado_civil = Item.objects.soltero()
            sacerdote.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(sacerdote).pk,
                object_id=sacerdote.id,
                object_repr=unicode(sacerdote),
                action_flag=ADDITION,
                change_message="Creo un sacerdote")
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(success_url)

        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_sacerdote': form_sacerdote, 'form_usuario': form_usuario}
            return render(request, template_name, ctx)

    else:
        form_sacerdote = SacerdoteForm()
        form_usuario = UsuarioSacerdoteForm()
        ctx = {'form_sacerdote': form_sacerdote, 'form_usuario': form_usuario}
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
                messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
                return HttpResponseRedirect(success_url)

            else:
                messages.error(request, MENSAJE_ERROR)
                ctx = {'form_sacerdote': form_sacerdote, 'form_usuario': form_usuario, 'object': sacerdote}
                return render(request, template_name, ctx)

        else:
            form_sacerdote = SacerdoteForm(instance=sacerdote)
            form_usuario = UsuarioSacerdoteForm(instance=sacerdote.user)
            ctx = {'form_sacerdote': form_sacerdote, 'form_usuario': form_usuario, 'object': sacerdote}
            return render(request, template_name, ctx)


class SacerdoteListView(PaginacionMixin, ListView):
    model = PerfilUsuario
    template_name = 'usuario/sacerdote_list.html'
    queryset = PerfilUsuario.objects.sacerdote()
    paginate_by = 10

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_sacerdote', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(SacerdoteListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        name = self.request.GET.get('q', '')
        if (name != ''):
            # name = ' '.join(name.split())
            name = ''.join((c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
            return PerfilUsuario.objects.sacerdote().filter(
                Q(nombres_completos__icontains=name) |
                Q(dni=name)).order_by('user__last_name')
        else:
            return PerfilUsuario.objects.sacerdote().order_by('user__last_name')


@login_required(login_url='/login/')
@permission_required('sacramentos.add_libro', login_url='/login/',
                     raise_exception=permission_required)
def libro_create_view(request):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    if (request.method == 'POST'):
        form_libro = LibroForm(request.POST, request=request)

        if form_libro.is_valid():
            libro = form_libro.save(commit=False)
            libro.parroquia = parroquia
            ultimo_libro = Libro.objects.ultimo_libro(parroquia, libro.tipo_libro)
            if ultimo_libro:
                libro.numero_libro = int(ultimo_libro.numero_libro) + 1
            else:
                libro.numero_libro = 1

            libro.nombre = u'%s%s%s' % (libro.tipo_libro.title(), libro.fecha_apertura.year, libro.numero_libro)
            libro.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(libro).pk,
                object_id=libro.id,
                object_repr=unicode(libro),
                action_flag=ADDITION,
                change_message="Creo un libro")
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(reverse_lazy('libro_list'))
        else:
            ctx = {'form_libro': form_libro}
            messages.error(request, MENSAJE_ERROR)
            return render(request, 'libro/libro_form.html', ctx)
    else:
        form_libro = LibroForm()
    ctx = {'form_libro': form_libro}
    return render(request, 'libro/libro_form.html', ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_libro', login_url='/login/',
                     raise_exception=permission_required)
def libro_update_view(request, pk):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    libro = get_object_or_404(Libro, pk=pk)

    if request.method == 'POST':
        form_libro = LibroForm(request.POST, instance=libro, request=request)

        if form_libro.is_valid():
            form_libro.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(libro).pk,
                object_id=libro.id,
                object_repr=unicode(libro.tipo_libro),
                action_flag=CHANGE,
                change_message="Libro actualizado")
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(reverse_lazy('libro_list'))

        else:
            ctx = {'form_libro': form_libro, 'object': libro}
            messages.error(request, MENSAJE_ERROR)
            return render(request, 'libro/libro_form.html', ctx)
    else:
        form_libro = LibroForm(instance=libro)
    ctx = {'form_libro': form_libro, 'object': libro}
    return render(request, 'libro/libro_form.html', ctx)


class LibroListView(PaginacionMixin, ListView):
    model = Libro
    template_name = 'libro/libro_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                return Libro.objects.filter(parroquia=parroquia, nombre__icontains=name).order_by('-principal',
                                                                                                  'tipo_libro',
                                                                                                  'numero_libro',
                                                                                                  'nombre')
            else:
                return Libro.objects.filter(parroquia=parroquia).order_by('-principal', 'tipo_libro', 'numero_libro',
                                                                          'nombre')
        else:
            raise PermissionDenied

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_libro', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(LibroListView, self).dispatch(*args, **kwargs)

# VISTAS PARA ADMIN DE BAUTISMO

@login_required(login_url='/login/')
@permission_required('sacramentos.add_bautismo', login_url='/login/',
                     raise_exception=permission_required)
def bautismo_create_view(request):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    usuario = request.user

    if (request.method == 'POST' ):
        formBautismo = BautismoForm(request, request.POST)
        formBautismo.fields['bautizado'].queryset = PerfilUsuario.objects.feligres()

        if formBautismo.is_valid():
            bautismo = formBautismo.save(commit=False)
            libro = bautismo.libro

            if libro.esta_vacio():
                bautismo.pagina = libro.primera_pagina
                bautismo.numero_acta = libro.primera_acta
            else:
                bautismo.asignar_numero_acta(libro)
            # ultimo_bautismo=Bautismo.objects.filter(libro=libro,parroquia=parroquia).latest('created')
            # num=ultimo_bautismo.numero_acta
            # pagina=ultimo_bautismo.pagina
            # bautismo.numero_acta=num+1

            # if bautismo.numero_acta%2 == 0:
            # 	bautismo.pagina=pagina
            # else:
            # 	bautismo.pagina=pagina+1

            bautismo.parroquia = parroquia
            bautismo.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(bautismo).pk,
                object_id=bautismo.id,
                object_repr=unicode(bautismo),
                action_flag=ADDITION,
                change_message='Se creo bautismo')
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect('/bautismo')

        else:
            bautizado = request.POST.get('bautizado')
            celebrante = request.POST.get('celebrante')
            formBautismo = BautismoForm(request, request.POST)
            formBautismo.fields['bautizado'].queryset = PerfilUsuario.objects.filter(id=bautizado)
            formBautismo.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=celebrante)
            messages.error(request, MENSAJE_ERROR)
            ctx = {'formBautismo': formBautismo, 'tipo_sacramento': 'bautismo'}
            return render(request, 'bautismo/bautismo_form.html', ctx)
    else:
        formBautismo = BautismoForm(request)
    ctx = {'formBautismo': formBautismo, 'tipo_sacramento': 'bautismo'}
    return render(request, 'bautismo/bautismo_form.html', ctx)

@login_required(login_url='/login/')
@permission_required('sacramentos.change_bautismo', login_url='/login/', raise_exception=permission_required)
def bautismo_update_view(request, pk):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    usuario = request.user
    bautismo = get_object_or_404(Bautismo, pk=pk)
    notas = NotaMarginal.objects.filter(bautismo=bautismo)

    if request.method == 'POST':
        bautismo_form = BautismoForm(request, request.POST, instance=bautismo)
        bautismo_form.fields['celebrante'].queryset = PerfilUsuario.objects.sacerdote()
        bautismo_form.fields['bautizado'].queryset = PerfilUsuario.objects.feligres()
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
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect('/bautismo')
        else:
            bautismo_form.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=bautismo.celebrante.id)
            bautismo_form.fields['bautizado'].queryset = PerfilUsuario.objects.filter(id=bautismo.bautizado.id)
            messages.error(request, MENSAJE_ERROR)
            ctx = {'formBautismo': bautismo_form, 'notas': notas, 'object': bautismo, 'tipo_sacramento': 'bautismo'}
            return render(request, 'bautismo/bautismo_form.html', ctx)
    else:
        bautismo_form = BautismoForm(request, instance=bautismo)
        ctx = {'formBautismo': bautismo_form, 'notas': notas, 'object': bautismo, 'tipo_sacramento': 'bautismo'}
        return render(request, 'bautismo/bautismo_form.html', ctx)


class BautismoListView(PaginacionMixin, ListView):
    model = Bautismo
    template_name = 'bautismo/bautismo_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                name = ''.join(
                    (c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
                return Bautismo.objects.filter(parroquia=parroquia).filter(
                    Q(bautizado__nombres_completos__icontains=name) |
                    Q(bautizado__dni=name)).order_by('bautizado__user__last_name')
            else:
                return Bautismo.objects.filter(parroquia=parroquia).order_by('bautizado__user__last_name')
        else:
            raise PermissionDenied

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
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    usuario = request.user
    if request.method == 'POST':
        form_eucaristia = EucaristiaForm(request, request.POST)
        form_eucaristia.fields['feligres'].queryset = PerfilUsuario.objects.feligres()
        form_eucaristia.fields['celebrante'].queryset = PerfilUsuario.objects.sacerdote()
        if form_eucaristia.is_valid():
            eucaristia = form_eucaristia.save(commit=False)
            tipo_sacramento = u'Eucaristia'
            eucaristia.tipo_sacramento = tipo_sacramento
            libro = eucaristia.libro

            if libro.esta_vacio():
                eucaristia.pagina = libro.primera_pagina
                eucaristia.numero_acta = libro.primera_acta
            else:
                eucaristia.asignar_numero_acta(libro)
            # ultimo_eucaristia=Eucaristia.objects.filter(libro=libro,parroquia=parroquia).latest('created')
            # num=ultimo_eucaristia.numero_acta
            # pagina=ultimo_eucaristia.pagina
            # eucaristia.numero_acta=num+1
            # if eucaristia.numero_acta%2 == 0:
            # 	eucaristia.pagina=pagina
            # else:
            # 	eucaristia.pagina=pagina+1

            eucaristia.parroquia = parroquia
            eucaristia.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(eucaristia).pk,
                object_id=eucaristia.id,
                object_repr=unicode(eucaristia),
                action_flag=ADDITION,
                change_message='Se creo eucaristia')
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(reverse_lazy('eucaristia_list'))

        else:
            id_feligres = request.POST.get('feligres')
            id_celebrante = request.POST.get('celebrante')
            form_eucaristia = EucaristiaForm(request, request.POST)
            form_eucaristia.fields['feligres'].queryset = PerfilUsuario.objects.filter(id=id_feligres)
            form_eucaristia.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=id_celebrante)
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_eucaristia': form_eucaristia, 'tipo_sacramento': 'eucaristia'}
            return render(request, 'eucaristia/eucaristia_form.html', ctx)
    else:
        form_eucaristia = EucaristiaForm(request)
        ctx = {'form_eucaristia': form_eucaristia, 'tipo_sacramento': 'eucaristia'}
        return render(request, 'eucaristia/eucaristia_form.html', ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_eucaristia', login_url='/login/',
                     raise_exception=permission_required)
def eucaristia_update_view(request, pk):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    usuario = request.user
    eucaristia = get_object_or_404(Eucaristia, pk=pk)

    if (request.method == 'POST'):
        form_eucaristia = EucaristiaForm(request, request.POST, instance=eucaristia)
        form_eucaristia.fields['feligres'].queryset = PerfilUsuario.objects.feligres()
        if form_eucaristia.is_valid():
            form_eucaristia.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(eucaristia).pk,
                object_id=eucaristia.id,
                object_repr=unicode(eucaristia),
                action_flag=CHANGE,
                change_message='Primera Comunión actualizada')
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(reverse_lazy('eucaristia_list'))
        else:
            id_feligres = request.POST.get('feligres')
            id_celebrante = request.POST.get('celebrante')
            form_eucaristia = EucaristiaForm(request, request.POST, instance=eucaristia)
            form_eucaristia.fields['feligres'].queryset = PerfilUsuario.objects.filter(id=id_feligres)
            form_eucaristia.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=id_celebrante)
            messages.error(request, MENSAJE_ERROR)

    else:
        form_eucaristia = EucaristiaForm(request, instance=eucaristia)
        form_eucaristia.fields['feligres'].queryset = PerfilUsuario.objects.filter(id=eucaristia.feligres.id)
        form_eucaristia.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=eucaristia.celebrante.id)
    ctx = {'form_eucaristia': form_eucaristia, 'object': eucaristia, 'tipo_sacramento': 'eucaristia'}
    return render(request, 'eucaristia/eucaristia_form.html', ctx)


class EucaristiaListView(PaginacionMixin, ListView):
    model = Eucaristia
    template_name = 'eucaristia/eucaristia_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                name = ''.join(
                    (c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
                return Eucaristia.objects.filter(parroquia=parroquia).filter(
                    Q(feligres__nombres_completos__icontains=name) |
                    Q(feligres__dni=name)).order_by('feligres__user__last_name')
            else:
                return Eucaristia.objects.filter(parroquia=parroquia).order_by('feligres__user__last_name')
        else:
            raise PermissionDenied


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
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    usuario = request.user
    confirmado = PerfilUsuario.objects.feligres()
    celebrante = PerfilUsuario.objects.sacerdote()
    if (request.method == 'POST'):
        form_confirmacion = ConfirmacionForm(request, request.POST)
        form_confirmacion.fields['confirmado'].queryset = PerfilUsuario.objects.feligres()
        form_confirmacion.fields['celebrante'].queryset = PerfilUsuario.objects.sacerdote()

        if form_confirmacion.is_valid():
            confirmacion = form_confirmacion.save(commit=False)
            confirmacion.tipo_sacramento = 'Confirmacion'
            libro = confirmacion.libro

            if libro.esta_vacio():
                confirmacion.pagina = libro.primera_pagina
                confirmacion.numero_acta = libro.primera_acta

            else:
                confirmacion.asignar_numero_acta(libro)
            # ultima_confirmacion=Confirmacion.objects.filter(libro=libro,parroquia=parroquia).latest('created')
            # num=ultima_confirmacion.numero_acta
            # confirmacion.numero_acta=num+1
            # pagina=ultima_confirmacion.pagina
            # if confirmacion.numero_acta%2 == 0:
            # 	confirmacion.pagina=pagina
            # else:
            # 	confirmacion.pagina=pagina+1

            confirmacion.parroquia = parroquia
            confirmacion.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(confirmacion).pk,
                object_id=confirmacion.id,
                object_repr=unicode(confirmacion),
                action_flag=ADDITION,
                change_message='Se creo bautismo')
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect('/confirmacion')

        else:
            id_confirmado = request.POST.get('confirmado')
            id_celebrante = request.POST.get('celebrante')
            form_confirmacion = ConfirmacionForm(request, request.POST)
            form_confirmacion.fields['confirmado'].queryset = PerfilUsuario.objects.filter(id=id_confirmado)
            form_confirmacion.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=id_celebrante)

            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_confirmacion': form_confirmacion, 'tipo_sacramento': 'confirmacion'}
            return render(request, 'confirmacion/confirmacion_form.html', ctx)

    else:
        form_confirmacion = ConfirmacionForm(request)
    ctx = {'form_confirmacion': form_confirmacion, 'tipo_sacramento': 'confirmacion'}
    return render(request, 'confirmacion/confirmacion_form.html', ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_confirmacion', login_url='/login/',
                     raise_exception=permission_required)
def confirmacion_update_view(request, pk):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    confirmacion = get_object_or_404(Confirmacion, pk=pk)

    if request.method == 'POST':
        form_confirmacion = ConfirmacionForm(request, request.POST, instance=confirmacion)
        form_confirmacion.fields['confirmado'].queryset = PerfilUsuario.objects.feligres()
        form_confirmacion.fields['celebrante'].queryset = PerfilUsuario.objects.sacerdote()

        if form_confirmacion.is_valid():
            form_confirmacion.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(confirmacion).pk,
                object_id=confirmacion.id,
                object_repr=unicode(confirmacion),
                action_flag=CHANGE,
                change_message='Confirmacion actualizado')
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(reverse_lazy('confirmacion_list'))
        else:
            id_confirmado = request.POST.get('confirmado')
            id_celebrante = request.POST.get('celebrante')
            form_confirmacion = ConfirmacionForm(request, request.POST, instance=confirmacion)
            form_confirmacion.fields['confirmado'].queryset = PerfilUsuario.objects.filter(id=id_confirmado)
            form_confirmacion.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=id_celebrante)
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_confirmacion': form_confirmacion, 'object': confirmacion, 'tipo_sacramento': 'confirmacion'}
            return render(request, 'confirmacion/confirmacion_form.html', ctx)
    else:
        form_confirmacion = ConfirmacionForm(request, instance=confirmacion)
        form_confirmacion.fields['confirmado'].queryset = PerfilUsuario.objects.filter(id=confirmacion.confirmado.id)
        form_confirmacion.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=confirmacion.celebrante.id)
    ctx = {'form_confirmacion': form_confirmacion, 'object': confirmacion, 'tipo_sacramento': 'confirmacion'}
    return render(request, 'confirmacion/confirmacion_form.html', ctx)


class ConfirmacionListView(PaginacionMixin, ListView):
    model = Confirmacion
    template_name = 'confirmacion/confirmacion_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                name = ''.join(
                    (c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
                return Confirmacion.objects.filter(parroquia=parroquia).filter(
                    Q(confirmado__nombres_completos__icontains=name) |
                    Q(confirmado__dni=name)).order_by('confirmado__user__last_name')
            else:
                return Confirmacion.objects.filter(parroquia=parroquia).order_by('confirmado__user__last_name')
        else:
            raise PermissionDenied


    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_confirmacion', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(ConfirmacionListView, self).dispatch(*args, **kwargs)


# VISTAS PARA ADMIN MATRIMONIO

@login_required(login_url='/login/')
@permission_required('sacramentos.add_matrimonio', login_url='/login/',
                     raise_exception=permission_required)
def matrimonio_create_view(request):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    if (request.method == 'POST'):
        form_matrimonio = MatrimonioForm(request, request.POST)
        form_matrimonio.fields['novio'].queryset = PerfilUsuario.objects.male()
        form_matrimonio.fields['novia'].queryset = PerfilUsuario.objects.female()
        form_matrimonio.fields['celebrante'].queryset = PerfilUsuario.objects.sacerdote()

        if form_matrimonio.is_valid():
            matrimonio = form_matrimonio.save(commit=False)
            matrimonio.tipo_sacramento = 'Matrimonio'
            novio = matrimonio.novio
            novia = matrimonio.novia
            libro = matrimonio.libro

            if libro.esta_vacio():
                matrimonio.pagina = libro.primera_pagina
                matrimonio.numero_acta = libro.primera_acta
            else:
                ultimo_matrimonio = Matrimonio.objects.filter(parroquia=parroquia).latest('created')
                num = ultimo_matrimonio.numero_acta
                pagina = ultimo_matrimonio.pagina
                matrimonio.pagina = pagina + 1
                matrimonio.numero_acta = num + 1

            novio.estado_civil = Item.objects.casado()
            novia.estado_civil = Item.objects.casado()
            novio.save()
            novia.save()
            matrimonio.novio = novio
            matrimonio.novia = novia
            matrimonio.parroquia = parroquia
            matrimonio.vigente = True
            matrimonio.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
                object_id=matrimonio.id,
                object_repr=unicode(matrimonio),
                action_flag=ADDITION,
                change_message='Se creo matrimonio')
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(reverse_lazy('matrimonio_list'))

        else:
            id_novio = request.POST.get('novio')
            id_novia = request.POST.get('novia')
            id_celebrante = request.POST.get('celebrante')
            form_matrimonio = MatrimonioForm(request, request.POST)
            form_matrimonio.fields['novio'].queryset = PerfilUsuario.objects.filter(id=id_novio)
            form_matrimonio.fields['novia'].queryset = PerfilUsuario.objects.filter(id=id_novia)
            form_matrimonio.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=id_celebrante)

            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_matrimonio': form_matrimonio, 'tipo_sacramento': 'matrimonio'}
            return render(request, 'matrimonio/matrimonio_form.html', ctx)

    else:

        form_matrimonio = MatrimonioForm(request)

    ctx = {'form_matrimonio': form_matrimonio, 'tipo_sacramento': 'matrimonio'}
    return render(request, 'matrimonio/matrimonio_form.html', ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_matrimonio', login_url='/login/',
                     raise_exception=permission_required)
def matrimonio_update_view(request, pk):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    matrimonio = get_object_or_404(Matrimonio, pk=pk)
    notas = NotaMarginal.objects.filter(matrimonio=matrimonio)

    if request.method == 'POST':
        form_matrimonio = MatrimonioForm(request, request.POST, instance=matrimonio)
        form_matrimonio.fields['novio'].queryset = PerfilUsuario.objects.male()
        form_matrimonio.fields['novia'].queryset = PerfilUsuario.objects.female()
        form_matrimonio.fields['celebrante'].queryset = PerfilUsuario.objects.sacerdote()

        if form_matrimonio.is_valid():
            matrimonio = form_matrimonio.save(commit=False)
            novio = matrimonio.novio
            novia = matrimonio.novia
            novio.estado_civil = Item.objects.casado()
            novia.estado_civil = Item.objects.casado()
            novio.save()
            novia.save()
            matrimonio.novio = novio
            matrimonio.novia = novia
            matrimonio.parroquia = parroquia
            matrimonio.vigente = True
            matrimonio.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
                object_id=matrimonio.id,
                object_repr=unicode(matrimonio),
                action_flag=CHANGE,
                change_message='Matrimonio actualizado')
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(reverse_lazy('matrimonio_list'))
        else:
            id_novio = request.POST.get('novio')
            id_novia = request.POST.get('novia')
            id_celebrante = request.POST.get('celebrante')
            form_matrimonio = MatrimonioForm(request, request.POST, instance=matrimonio)
            form_matrimonio.fields['novio'].queryset = PerfilUsuario.objects.filter(id=id_novio)
            form_matrimonio.fields['novia'].queryset = PerfilUsuario.objects.filter(id=id_novia)
            form_matrimonio.fields['celebrante'].queryset = PerfilUsuario.objects.filter(id=id_celebrante)
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form_matrimonio': form_matrimonio, 'notas': notas, 'object': matrimonio,
                   'tipo_sacramento': 'matrimonio'}
            return render(request, 'matrimonio/matrimonio_form.html', ctx)
    else:
        form_matrimonio = MatrimonioForm(request, instance=matrimonio)
        form_matrimonio.fields['novio'].queryset = PerfilUsuario.objects.filter(user__id=matrimonio.novio.user.id)
        form_matrimonio.fields['novia'].queryset = PerfilUsuario.objects.filter(user__id=matrimonio.novia.user.id)
        form_matrimonio.fields['celebrante'].queryset = PerfilUsuario.objects.filter(
            user__id=matrimonio.celebrante.user.id)

    ctx = {'form_matrimonio': form_matrimonio, 'notas': notas, 'object': matrimonio, 'tipo_sacramento': 'matrimonio'}
    return render(request, 'matrimonio/matrimonio_form.html', ctx)


class MatrimonioListView(PaginacionMixin, ListView):
    model = Matrimonio
    template_name = 'matrimonio/matrimonio_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                name = ''.join(
                    (c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
                return Matrimonio.objects.filter(parroquia=parroquia).filter(
                    Q(novio__nombres_completos__icontains=name) |
                    Q(novio__dni=name) |
                    Q(novia__nombres_completos__icontains=name) |
                    Q(novia__dni=name))
            else:
                return Matrimonio.objects.filter(parroquia=parroquia)
        else:
            raise PermissionDenied


    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_matrimonio', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(MatrimonioListView, self).dispatch(*args, **kwargs)


class MatrimonioNoVigenteListView(PaginacionMixin, ListView):
    model = Matrimonio
    template_name = 'matrimonio/matrimonio_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                name = ''.join(
                    (c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
                return Matrimonio.objects.filter(parroquia=parroquia, vigente=False).filter(
                    Q(novio__nombres_completos__icontains=name) |
                    Q(novio__dni=name) |
                    Q(novia__nombres_completos__icontains=name) |
                    Q(novia__dni=name))
            else:
                return Matrimonio.objects.filter(parroquia=parroquia, vigente=False)
        else:
            raise PermissionDenied


    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_matrimonio', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(MatrimonioNoVigenteListView, self).dispatch(*args, **kwargs)


#Preguntar si esta función es ajax
@login_required(login_url='/login/')
@permission_required('sacramentos.delete_matrimonio', login_url='/login/',
                     raise_exception=permission_required)
def matrimonio_vigencia_view(request, pk):
    matrimonio = get_object_or_404(Matrimonio, pk=pk)
    if request.method == 'POST':
        novio = matrimonio.novio
        novia = matrimonio.novia
        novio.estado_civil = Item.objects.viudo()
        novia.estado_civil = Item.objects.viudo()
        novio.save()
        novia.save()
        matrimonio.vigente = False
        matrimonio.save()
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(matrimonio).pk,
            object_id=matrimonio.id,
            object_repr=unicode(matrimonio),
            action_flag=DELETION,
            change_message='Dado de baja matrimonio')
        messages.success(request, 'Se quitó la vigencia del matrimonio con éxito')
        return HttpResponse(json.dumps({'respuesta': True}), content_type='application/json')
    else:
        form = MatrimonioForm(request, instance=matrimonio)
        matrimonio.vigente = False
        matrimonio.save()

    ctx = {'form': form}
    return render(request, 'matrimonio/matrimonio_list.html', ctx)


@login_required(login_url='/login/')
def matrimonio_ajax_view(request):
    exito = False
    matrimonio = Matrimonio.objects.all()
    list_matrimonios = list()
    for m in matrimonio:
        novio = u'%s' % m.novio.user.get_full_name()
        novia = u'%s' % m.novia.user.get_full_name()
        list_matrimonios.append({'id': m.pk, 'novio': novio, 'novia': novia})
    ctx = {'list_matrimonios': list_matrimonios, 'exito': exito}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

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
    if request.method == 'POST':
        form_parroquia = ParroquiaForm(request.POST)
        form_direccion = DireccionForm(request.POST)
        form_direccion.fields['canton'].queryset = Item.objects.items_por_catalogo_cod('CANTONES')
        form_direccion.fields['parroquia'].queryset = Item.objects.items_por_catalogo_cod('PARROQUIAS')
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
            messages.success(request, MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(success_url)
        else:
            ctx = {'form_parroquia': form_parroquia, 'form_direccion': form_direccion}
            # messages.error(request, ctx)
            messages.error(request, MENSAJE_ERROR)
            return render(request, template_name, ctx)
    else:
        form_parroquia = ParroquiaForm()
        form_direccion = DireccionForm()
        ctx = {'form_parroquia': form_parroquia, 'form_direccion': form_direccion}
        return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_parroquia', login_url='/login/',
                     raise_exception=permission_required)
def parroquia_update_view(request, pk):
    template_name = 'parroquia/parroquia_form.html'
    success_url = '/parroquia/'
    parroquia = get_object_or_404(Parroquia, pk=pk)
    direccion = parroquia.direccion

    if request.method == 'POST':
        form_parroquia = ParroquiaForm(request.POST, instance=parroquia)
        form_direccion = DireccionForm(request.POST, instance=direccion)
        form_direccion.fields['canton'].queryset = Item.objects.items_por_catalogo_cod('CANTONES')
        form_direccion.fields['parroquia'].queryset = Item.objects.items_por_catalogo_cod('PARROQUIAS')
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
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(success_url)
        else:
            ctx = {'form_parroquia': form_parroquia, 'form_direccion': form_direccion}
            messages.error(request, MENSAJE_ERROR)
            return render(request, template_name, ctx)
    else:
        form_parroquia = ParroquiaForm(instance=parroquia)
        form_direccion = DireccionForm(instance=direccion)
        form_direccion.fields['canton'].queryset = Item.objects.cantones().filter(padre=direccion.provincia)
        form_direccion.fields['parroquia'].queryset = Item.objects.parroquias().filter(padre=direccion.canton)
        ctx = {'form_parroquia': form_parroquia, 'form_direccion': form_direccion, 'object': parroquia}
        return render(request, template_name, ctx)


class ParroquiaListView(BusquedaMixin, ListView):
    model = Parroquia
    template_name = 'parroquia/parroquia_list.html'
    paginate_by = 10

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_parroquia', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(ParroquiaListView, self).dispatch(*args, **kwargs)


class DirectorioParroquiasListView(BusquedaMixin, ListView):
    model = Parroquia
    template_name = 'directorio/directorio_parroquias.html'
    paginate_by = 10

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        return super(DirectorioParroquiasListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Parroquia.objects.values_list('nombre', 'direccion__telefono')


@login_required(login_url='/login/')
@permission_required('sacramentos.add_intencion', login_url='/login/',
                     raise_exception=permission_required)
def intencion_create_view(request):
    template_name = 'intencion/intencion_form.html'
    success_url = '/intencion/'
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    if request.method == 'POST':
        form_intencion = IntencionForm(request.POST)
        form_intencion.fields['iglesia'].queryset = Iglesia.objects.filter(parroquia=parroquia)

        if form_intencion.is_valid():
            fecha = request.POST.get('fecha')
            hora = request.POST.get('hora')
            individual = request.POST.get('individual')
            intencion = form_intencion.save(commit=False)

            intencion_unica = Intencion.objects.filter(fecha=fecha, hora=hora, parroquia=parroquia, individual=True)
            intenciones_colectivas = Intencion.objects.filter(fecha=fecha, hora=hora, parroquia=parroquia)
            if intencion_unica:
                messages.error(request, MENSAJE_ERROR)
                form_intencion.errors['individual'] = ErrorList([
                    u'No se puede puede crear una intención, porque ya existe una intención única para el dia y hora indicado'])
                ctx = {'form': form_intencion}
                return render(request, template_name, ctx)
            elif intenciones_colectivas and individual:
                messages.error(request, MENSAJE_ERROR)
                form_intencion.errors['individual'] = ErrorList([
                    u'No se puede puede crear una intención única, porque ya existen intenciones colectivas para el dia y hora indicado'])
                ctx = {'form': form_intencion, 'object': intencion}
                return render(request, template_name, ctx)
            else:
                # messages.success(request, 'Creado exitosamente: %s' %individual)
                intencion.parroquia = parroquia
                intencion.save()
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(intencion).pk,
                    object_id=intencion.id,
                    object_repr=unicode(intencion),
                    action_flag=ADDITION,
                    change_message="Creo una intencion")
                messages.success(request, MENSAJE_EXITO_CREACION)
                return HttpResponseRedirect(success_url)

        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form': form_intencion}
            return render(request, template_name, ctx)
    else:
        form_intencion = IntencionForm()
        form_intencion.fields['iglesia'].queryset = Iglesia.objects.filter(parroquia=parroquia)
        try:
            form_intencion.fields['iglesia'].initial = Iglesia.objects.get(principal=True, parroquia=parroquia)
        except ObjectDoesNotExist:
            mensaje = 'No tiene configurada una Iglesia principal. Configurela '
            msg = mark_safe(u"%s %s" % (
            mensaje, '<a class="btn btn-primary" href="#id_modal_iglesia" data-toggle="modal">aqui</a>'))
            messages.info(request, msg)
        ctx = {'form': form_intencion}
        return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_intencion', login_url='/login/',
                     raise_exception=permission_required)
def intencion_edit_view(request, pk):
    parroquia = request.session.get('parroquia')
    if not parroquia:
        raise PermissionDenied

    intencion = get_object_or_404(Intencion, pk=pk)

    template_name = 'intencion/intencion_form.html'
    success_url = '/intencion/'
    if request.method == 'POST':
        form_intencion = IntencionForm(request.POST, instance=intencion)
        form_intencion.fields['iglesia'].queryset = Iglesia.objects.filter(parroquia=parroquia)

        if form_intencion.is_valid():
            fecha = request.POST.get('fecha')
            hora = request.POST.get('hora')
            individual = request.POST.get('individual')
            intencion_unica = Intencion.objects.filter(fecha=fecha, hora=hora, parroquia=intencion.parroquia,
                                                         individual=True).exclude(pk=pk)
            intenciones_colectivas = Intencion.objects.filter(fecha=fecha, hora=hora,
                                                                parroquia=intencion.parroquia).exclude(pk=pk)
            if intencion_unica:
                messages.error(request, MENSAJE_ERROR)
                form_intencion.errors['individual'] = ErrorList([
                    u'No se puede puede editar la intención, porque ya existe una intención única para el dia y hora indicados'])
                ctx = {'form': form_intencion, 'object': intencion}
                return render(request, template_name, ctx)
            elif intenciones_colectivas and individual:
                messages.error(request, MENSAJE_ERROR)
                form_intencion.errors['individual'] = ErrorList([
                    u'No se puede puede editar la intención como única, porque ya existen intenciones colectivas para el dia y hora indicados'])
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
                messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
                return HttpResponseRedirect(success_url)
        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form': form_intencion}
            return render(request, template_name, ctx)
    else:
        form_intencion = IntencionForm(instance=intencion)
        ctx = {'form': form_intencion, 'object': intencion}
        return render(request, template_name, ctx)


class IntencionListView(BusquedaMixin, ListView):
    model = Intencion
    template_name = 'intencion/intencion_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                return Intencion.objects.filter(oferente__icontains=name, parroquia=parroquia).order_by('-fecha',
                                                                                                          'hora')
            else:
                return Intencion.objects.filter(parroquia=parroquia).order_by('-fecha', 'hora')
        else:
            raise PermissionDenied

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_intencion', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(IntencionListView, self).dispatch(*args, **kwargs)


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
                asignacion = AsignacionParroquia.objects.get(persona__id=persona,
                                                             parroquia__id=parroquia)
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
            messages.error(request, MENSAJE_ERROR)
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
        form.fields['persona'].queryset = PerfilUsuario.objects.all()

        if form.is_valid() and form_periodo.is_valid():
            try:
                asignacion = AsignacionParroquia.objects.get(persona__id=persona,
                                                             parroquia__id=parroquia.id)
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
                messages.success(request, MENSAJE_EXITO_CREACION)
                return HttpResponseRedirect(success_url)

        else:
            messages.error(request, MENSAJE_ERROR)
            form = AsignarParroquiaForm(parroquias, request.POST)
            form.fields['persona'].queryset = PerfilUsuario.objects.filter(id=persona)
            ctx = {'form': form, 'form_periodo': form_periodo, 'object': parroquia}
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
    asignacion = get_object_or_404(AsignacionParroquia, pk=pk)
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
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
            return HttpResponseRedirect(success_url)
        else:
            messages.error(request, MENSAJE_ERROR)
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
            periodo_activo = PeriodoAsignacionParroquia.objects.filter(asignacion=asignacion, estado=True)
            periodo_activo_otra_parroquia = PeriodoAsignacionParroquia.objects.filter(
                asignacion__persona=asignacion.persona, estado=True).exclude(asignacion__parroquia=asignacion.parroquia)
            if periodo_activo:
                messages.error(request, MENSAJE_ERROR)
                form.errors['estado'] = ErrorList(["El sacerdote ya está asignado a la parroquia"])
                ctx = {'form': form, 'object': asignacion}
                return render(request, template_name, ctx)

            elif periodo_activo_otra_parroquia:
                messages.error(request, MENSAJE_ERROR)
                form.errors['estado'] = ErrorList(["El sacerdote tiene un periodo activo en otra parroquia"])
                ctx = {'form': form, 'object': asignacion}
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
                messages.success(request, MENSAJE_EXITO_CREACION)
                return HttpResponseRedirect(success_url)

        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form': form, 'object': asignacion}
            return render(request, template_name, ctx)

    else:
        form = PeriodoAsignacionParroquiaForm()
        ctx = {'form': form, 'object': asignacion}
        return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_asignarsacerdote', login_url='/login/',
                     raise_exception=permission_required)
def parroco_periodos_asignacion_update(request, pk):
    periodo = get_object_or_404(PeriodoAsignacionParroquia, pk=pk)
    template_name = 'parroquia/periodo_asignacion_form.html'
    success_url = u'/parroco/periodos/asignacion/%s/' % periodo.asignacion.id

    if request.method == 'POST':
        estado = request.POST.get('estado')
        form = PeriodoAsignacionParroquiaForm(request.POST, instance=periodo)
        if form.is_valid():

            periodo_activo = PeriodoAsignacionParroquia.objects.filter(asignacion=periodo.asignacion,
                                                                       estado=True).exclude(id=periodo.id)
            periodo_activo_otra_parroquia = PeriodoAsignacionParroquia.objects.filter(
                asignacion__persona=periodo.asignacion.persona, estado=True).exclude(
                asignacion__parroquia=periodo.asignacion.parroquia)

            if periodo_activo:
                messages.error(request, MENSAJE_ERROR)
                form.errors['estado'] = ErrorList(["El sacerdote ya está asignado a la parroquia"])
                ctx = {'form': form, 'periodo': periodo, 'object': periodo.asignacion}
                return render(request, template_name, ctx)

            elif periodo_activo_otra_parroquia:
                messages.error(request, MENSAJE_ERROR)
                form.errors['estado'] = ErrorList(["El sacerdote tiene un periodo activo en otra parroquia"])
                ctx = {'form': form, 'periodo': periodo, 'object': periodo.asignacion}
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
                messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
                return HttpResponseRedirect(success_url)
        else:
            messages.error(request, MENSAJE_ERROR)
            ctx = {'form': form, 'periodo': periodo, 'object': periodo.asignacion}
            return render(request, template_name, ctx)

    else:
        form = PeriodoAsignacionParroquiaForm(instance=periodo)
        ctx = {'form': form, 'periodo': periodo, 'object': periodo.asignacion}
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
    global rango
    template_name = 'parroquia/asignar_parroquia_list.html'
    parroquia = get_object_or_404(Parroquia, pk=pk)
    q = request.GET.get('q', '')
    if q:
        asignaciones = AsignacionParroquia.objects.filter(parroquia=parroquia,
                                                          persona__user__groups__name='Sacerdote').filter(
            Q(persona__nombres_completos__icontains=q) |
            Q(persona__dni__icontains=q)
        )
    else:
        asignaciones = AsignacionParroquia.objects.filter(parroquia=parroquia, persona__user__groups__name='Sacerdote')

    paginator = Paginator(asignaciones, 10)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    # pagina_actual = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    numero_paginas = paginator.num_pages
    pagina_actual = page

    if numero_paginas > 1:
        is_paginated = True
    else:
        is_paginated = False

    if numero_paginas > 5:
        resta = numero_paginas - pagina_actual

        if pagina_actual <= 2:
            rango = [x for x in range(1, 6)]
        else:
            if resta > 1:
                rango = [pagina_actual - 2, pagina_actual - 1, pagina_actual, pagina_actual + 1, pagina_actual + 2]
            elif resta <= 1:
                rango = [x for x in range(numero_paginas - 4, numero_paginas + 1)]
    elif numero_paginas <= 5:
        rango = [x for x in range(1, numero_paginas + 1)]

    ctx = {'page_obj': page_obj, 'object_list': asignaciones, 'parroquia': parroquia, 'rango': rango, 'q': q,
           'is_paginated': is_paginated}
    return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_asignarsecretaria', login_url='/login/')
def asignar_secretaria_create(request):
    template_name = "parroquia/asignar_secretaria_form.html"
    success_url = '/asignar/secretaria/'
    usuario = request.user
    try:
        parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user,
                                                           estado=True).asignacion.parroquia
        if request.method == 'POST':
            perfil = get_object_or_404(PerfilUsuario, pk=request.POST.get('persona'))
            persona = PerfilUsuario.objects.feligres()
            form = AsignarSecretariaForm(usuario, persona, request.POST.get('estado'), request.POST)
            form_periodo = PeriodoAsignacionParroquiaForm(request.POST)

            if form.is_valid() and form_periodo.is_valid():
                try:
                    periodo_asignacion = PeriodoAsignacionParroquia.objects.get(asignacion__persona=perfil, estado=True)
                    form.errors["persona"] = ErrorList([u'El usuario elegido ya cuenta con una asignación activa.'])
                    messages.error(request, MENSAJE_ERROR)
                    form.fields['persona'].queryset = PerfilUsuario.objects.filter(id=perfil.id)
                    ctx = {'form': form, 'form_periodo': form_periodo}
                    return render(request, template_name, ctx)
                except ObjectDoesNotExist:
                    try:
                        asignacion = PeriodoAsignacionParroquia.objects.get(asignacion__persona=perfil, estado=False,
                                                                            asignacion__parroquia=parroquia)
                        mensaje = u"El usuario elegido tiene un periodo desactivo, proceda a activarlo desde el siguiente "
                        msg = mark_safe(u"%s %s" % (
                        mensaje, '<a href="/asignar/secretaria/' + str(asignacion.id) + '/" >formulario</a>'))
                        form.errors["persona"] = ErrorList([msg])
                        messages.error(request, MENSAJE_ERROR)
                        ctx = {'form': form, 'form_periodo': form_periodo}
                        return render(request, template_name, ctx)
                    except ObjectDoesNotExist:
                        asig = form.save()
                        periodo = form_periodo.save(commit=False)
                        periodo.asignacion = asig
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
                        messages.success(request, MENSAJE_EXITO_CREACION)
                        return HttpResponseRedirect(success_url)
            else:
                if request.POST.get('persona'):
                    messages.error(request, MENSAJE_ERROR)
                    form_email = EmailForm()
                    personas = PerfilUsuario.objects.filter(id=request.POST.get('persona'))
                    form = AsignarSecretariaForm(usuario, personas, request.POST.get('estado'), request.POST)
                    ctx = {'form': form, 'form_periodo': form_periodo, 'form_email': form_email, 'persona': perfil}
                else:
                    messages.error(request, MENSAJE_ERROR)
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
        parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user=request.user,
                                                           estado=True).asignacion.parroquia

        if periodo.asignacion.parroquia == parroquia and periodo.asignacion.persona.user != request.user:

            usuario = request.user
            if request.method == 'POST':
                persona = PerfilUsuario.objects.feligres()
                form = AsignarSecretariaForm(usuario, persona, periodo.asignacion.persona.user.is_staff, request.POST,
                                             instance=periodo.asignacion)
                form_periodo = PeriodoAsignacionParroquiaForm(request.POST, instance=periodo)
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
                    periodo.asignacion = asig
                    periodo.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ContentType.objects.get_for_model(periodo.asignacion).pk,
                        object_id=periodo.asignacion.id,
                        object_repr=unicode(periodo.asignacion),
                        action_flag=ADDITION,
                        change_message="Asignacion parroquia y secretaria actualizado")
                    messages.success(request, MENSAJE_EXITO_ACTUALIZACION)
                    return HttpResponseRedirect(success_url)
                else:
                    if periodo.asignacion.persona:
                        messages.error(request, MENSAJE_ERROR)
                        persona = PerfilUsuario.objects.filter(user__id=periodo.asignacion.persona.user.id)
                        form = AsignarSecretariaForm(usuario, persona, periodo.asignacion.persona.user.is_staff,
                                                     request.POST, instance=periodo.asignacion)
                    else:
                        messages.error(request, MENSAJE_ERROR)
                        persona = PerfilUsuario.objects.none()
                        form = AsignarSecretariaForm(usuario, persona, request.POST, instance=periodo.asignacion)

                    ctx = {'form': form, 'form_periodo': form_periodo, 'object': periodo}
                    return render(request, template_name, ctx)
            else:
                if periodo.asignacion.persona:
                    persona = PerfilUsuario.objects.filter(user__id=periodo.asignacion.persona.user.id)
                    form = AsignarSecretariaForm(usuario, persona, periodo.asignacion.persona.user.is_staff,
                                                 instance=periodo.asignacion)
                else:
                    persona = PerfilUsuario.objects.none()
                    form = AsignarSecretariaForm(usuario, persona, periodo.asignacion.persona.user.is_staff,
                                                 instance=periodo.asignacion)

                form_periodo = PeriodoAsignacionParroquiaForm(instance=periodo)
                ctx = {'form': form, 'form_periodo': form_periodo, 'object': periodo}
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
        parroquia = PeriodoAsignacionParroquia.objects.get(estado=True,
                                                           asignacion__persona__user=request.user).asignacion.parroquia
        object_list = PeriodoAsignacionParroquia.objects.filter(asignacion__parroquia=parroquia,
                                                                asignacion__persona__user__groups__name='Secretaria')
        # object_list= AsignacionParroquia.objects.filter(parroquia=parroquia).exclude(persona__user__groups__name='Sacerdote')
        ctx = {'object_list': object_list, 'parroquia': parroquia}
        return render(request, template_name, ctx)
    except ObjectDoesNotExist:
        raise PermissionDenied


class SecretariaListView(ListView):
    model = PerfilUsuario
    template_name = 'parroquia/asignar_secretaria_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            name = self.request.GET.get('q', '')
            if (name != ''):
                # name = ' '.join(name.split())
                name = ''.join(
                    (c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
                return PeriodoAsignacionParroquia.objects.secretaria(parroquia).filter(
                    Q(asignacion__persona__nombres_completos__icontains=name) |
                    Q(asignacion__persona__dni=name)).order_by('asignacion__persona__user__last_name')
            else:
                return PeriodoAsignacionParroquia.objects.secretaria(parroquia).order_by(
                    'asignacion__persona__user__last_name')
        else:
            raise PermissionDenied

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('sacramentos.change_asignarsecretaria',
                                          login_url='/login/', raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(SecretariaListView, self).dispatch(*args, **kwargs)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_parametrizadiocesis', login_url='/login/',
                     raise_exception=permission_required)
@permission_required('sacramentos.change_parametrizadiocesis', login_url='/login/',
                     raise_exception=permission_required)
def parametriza_diocesis_create(request):
    try:
        objeto = ParametrizaDiocesis.objects.get(pk=1)
    except ObjectDoesNotExist:
        objeto = False

    if request.method == 'POST':
        if objeto:
            form_parametriza = ParametrizaDiocesisForm(request.POST, instance=objeto)
            form_direccion = DireccionForm(request.POST, instance=objeto.direccion)
        else:
            form_parametriza = ParametrizaDiocesisForm(request.POST)
            form_direccion = DireccionForm(request.POST)
        form_direccion.fields['canton'].queryset = Canton.objects.all()
        form_direccion.fields['parroquia'].queryset = ParroquiaCivil.objects.all()

        if form_parametriza.is_valid() and form_direccion.is_valid():
            parametriza = form_parametriza.save(commit=False)
            direccion = form_direccion.save()
            parametriza.direccion = direccion
            parametriza.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(parametriza).pk,
                object_id=parametriza.id,
                object_repr=unicode(parametriza),
                action_flag=CHANGE if objeto else ADDITION,
                change_message=MENSAJE_EXITO_ACTUALIZACION if objeto else MENSAJE_EXITO_CREACION)
            messages.success(request, MENSAJE_EXITO_ACTUALIZACION if objeto else MENSAJE_EXITO_CREACION)
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            ctx = {'form_parametriza': form_parametriza, 'form_direccion': form_direccion}
            messages.error(request, MENSAJE_ERROR)
            return render(request, 'parametriza/parametriza_form.html', ctx)
    else:
        if objeto:
            form_parametriza = ParametrizaDiocesisForm(instance=objeto)
            form_direccion = DireccionForm(instance=objeto.direccion)
            form_direccion.fields['canton'].queryset = Canton.objects.filter(provincia=objeto.direccion.provincia)
            form_direccion.fields['parroquia'].queryset = ParroquiaCivil.objects.filter(canton=objeto.direccion.canton)
        else:
            form_parametriza = ParametrizaDiocesisForm()
            form_direccion = DireccionForm()
        ctx = {'form_parametriza': form_parametriza, 'form_direccion': form_direccion, 'object': objeto}
        return render(request, 'parametriza/parametriza_form.html', ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_parametrizaparroquia', login_url='/login/',
                     raise_exception=permission_required)
@permission_required('sacramentos.change_parametrizaparroquia', login_url='/login/',
                     raise_exception=permission_required)
def parametriza_parroquia_create(request):
    usuario = request.user
    try:
        asignacion = AsignacionParroquia.objects.get(persona__user=usuario,
                                                     periodos__estado=True)
    except ObjectDoesNotExist:
        raise PermissionDenied

    p = ParametrizaParroquia.objects.filter(parroquia=asignacion.parroquia)
    of = ''
    for o in p:
        of = o
    if p:
        if request.method == 'POST':
            form_parametriza = ParametrizaParroquiaForm(usuario, request.POST, instance=of)
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
                ctx = {'form_parametriza': form_parametriza}
                messages.error(request, MENSAJE_ERROR)
                return render(request, 'parametriza/parroquia/parametriza_form.html', ctx)
        else:
            form_parametriza = ParametrizaParroquiaForm(usuario, instance=of)
            ctx = {'form_parametriza': form_parametriza, 'object': of}
            return render(request, 'parametriza/parroquia/parametriza_form.html', ctx)
    else:

        if (request.method == 'POST'):
            form_parametriza = ParametrizaParroquiaForm(usuario, request.POST)

            if form_parametriza.is_valid():
                parametriza = form_parametriza.save(commit=False)
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
                ctx = {'form_parametriza': form_parametriza}
                messages.error(request, MENSAJE_ERROR)
                return render(request, 'parametriza/parroquia/parametriza_form.html', ctx)
        else:
            form_parametriza = ParametrizaParroquiaForm(usuario)
            ctx = {'form_parametriza': form_parametriza}
            return render(request, 'parametriza/parroquia/parametriza_form.html', ctx)


# views para los LOGS del ekklesia
class LogListView(PaginacionMixin, ListView):
    model = LogEntry
    template_name = 'log/log_list.html'
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get('q', '')
        if (name != ''):
            name = ''.join((c for c in unicodedata.normalize('NFD', unicode(name)) if unicodedata.category(c) != 'Mn'))
            return LogEntry.objects.filter(user__username__icontains=name).order_by('user__username', '-action_time')
        else:
            return LogEntry.objects.all().order_by('user__username', '-action_time')

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
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


@login_required(login_url='/login/')
def libro_pdf(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    html = render_to_string('libro/libro.html', {'pagesize': 'A4', 'libro': libro},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_matrimonio', login_url='/login/',
                     raise_exception=permission_required)
def matrimonio_certificado(request, pk):
    matrimonio = get_object_or_404(Matrimonio, pk=pk)
    try:
        asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                     periodos__estado=True)
        p = ParametrizaDiocesis.objects.all()

    except ObjectDoesNotExist:
        raise PermissionDenied
    cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                           parroquia=asignacion.parroquia, periodos__estado=True)
    notas = NotaMarginal.objects.filter(matrimonio=matrimonio)
    html = render_to_string('matrimonio/matrimonio_certificado.html', {'pagesize': 'A4',
                                                                       'matrimonio': matrimonio, 'cura': cura,
                                                                       'notas': notas, 'asignacion': asignacion,
                                                                       'p': p},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_bautismo', login_url='/login/',
                     raise_exception=permission_required)
def bautismo_certificado(request, pk):
    bautismo = get_object_or_404(Bautismo, pk=pk)
    try:
        asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                     periodos__estado=True)
        p = ParametrizaDiocesis.objects.all()
    except ObjectDoesNotExist:
        raise PermissionDenied
    cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                           parroquia=asignacion.parroquia, periodos__estado=True)
    notas = NotaMarginal.objects.filter(bautismo=bautismo)
    html = render_to_string('bautismo/bautismo_certificado.html', {'pagesize': 'A4', 'bautismo': bautismo,
                                                                   'cura': cura, 'notas': notas,
                                                                   'asignacion': asignacion, 'p': p},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_bautismo', login_url='/login/',
                     raise_exception=permission_required)
def bautismo_acta(request, pk):
    bautismo = get_object_or_404(Bautismo, pk=pk)
    try:
        asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                     periodos__estado=True)
        p = ParametrizaDiocesis.objects.all()
    except ObjectDoesNotExist:
        raise PermissionDenied
    cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                           parroquia=asignacion.parroquia, periodos__estado=True)
    notas = NotaMarginal.objects.filter(bautismo=bautismo)
    html = render_to_string('bautismo/bautismo_acta.html', {'pagesize': 'A4', 'bautismo': bautismo,
                                                            'cura': cura, 'notas': notas, 'asignacion': asignacion,
                                                            'p': p}, context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_confirmacion', login_url='/login/',
                     raise_exception=permission_required)
def confirmacion_reporte(request, pk):
    confirmacion = get_object_or_404(Confirmacion, pk=pk)
    try:
        asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                     periodos__estado=True)
        p = ParametrizaDiocesis.objects.all()

    except ObjectDoesNotExist:
        raise PermissionDenied
    cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                           parroquia=asignacion.parroquia, periodos__estado=True)
    html = render_to_string('confirmacion/confirmacion_certificado.html',
                            {'pagesize': 'A4', 'confirmacion': confirmacion, 'cura': cura, 'asignacion': asignacion,
                             'p': p},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_eucaristia', login_url='/login/',
                     raise_exception=permission_required)
def eucaristia_reporte(request, pk):
    eucaristia = get_object_or_404(Eucaristia, pk=pk)
    try:
        asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                     periodos__estado=True)
        p = ParametrizaDiocesis.objects.all()
    except ObjectDoesNotExist:
        raise PermissionDenied
    cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                           parroquia=asignacion.parroquia, periodos__estado=True)
    # notas=NotaMarginal.objects.filter()
    html = render_to_string('eucaristia/eucaristia_certificado.html', {'pagesize': 'A4', 'eucaristia': eucaristia,
                                                                       'cura': cura, 'asignacion': asignacion, 'p': p},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_feligres', login_url='/login/',
                     raise_exception=permission_required)
def usuario_reporte_honorabilidad(request, pk):
    perfil = get_object_or_404(PerfilUsuario, pk=pk)
    # parroquia=AsignacionParroquia.objects.get(persona__user=request.user).parroquia
    try:
        asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                     periodos__estado=True)
        p = ParametrizaDiocesis.objects.all()
    except ObjectDoesNotExist:
        raise PermissionDenied
    cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                           parroquia=asignacion.parroquia, periodos__estado=True)
    html = render_to_string('usuario/certificado_honorabilidad.html', {'pagesize': 'A4', 'perfil': perfil,
                                                                       'cura': cura, 'asignacion': asignacion, 'p': p},
                            context_instance=RequestContext(request))
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
    anio_actual = request.GET.get('anio')
    # print("El año ingresado es: %d"%anio_actual)
    template_name = "reportes/reporte_anual_sacramentos_form.html"
    if anio_actual == anio_actual:

        if anio_actual:
            ninios1 = 0
            ninios7 = 0
            ninios = 0
            try:
                asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                             periodos__estado=True)
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied
            bautismos = Bautismo.objects.filter(fecha_sacramento__year=anio_actual,
                                                parroquia=asignacion.parroquia)
            num_bautizos = len(bautismos)
            for b in bautismos:
                print("Bautismos en 2013 son: %s" % (len(bautismos)))
                num_bautizos = len(bautismos)
                anios_bautizados = b.bautizado.fecha_nacimiento.year
                # print('años de los bautizados en año:%d son: %d' %(int(anio_actual),bautizados))
                resta = int(anio_actual) - anios_bautizados
                if (resta <= 1):
                    ninios1 = ninios1 + 1
                    print ("Niños hasta 1 año %s" % ninios1)
                elif (resta > 1 and resta <= 7):
                    ninios7 = ninios7 + 1
                    print('Niños de 1 a 7: %s' % ninios7)
                else:
                    ninios = ninios + 1
                    print('Niños mayores de 7: %s' % ninios)

            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=asignacion.parroquia, periodos__estado=True)
            # bautismos=Bautismo.objects.filter(fecha_sacramento__year=anio_actual).count()
            eucaristias = Eucaristia.objects.filter(fecha_sacramento__year=anio_actual,
                                                    parroquia=asignacion.parroquia).count()
            confirmaciones = Confirmacion.objects.filter(fecha_sacramento__year=anio_actual,
                                                         parroquia=asignacion.parroquia).count()
            catolicos = Matrimonio.objects.filter(fecha_sacramento__year=anio_actual,
                                                  tipo_matrimonio='Catolico', parroquia=asignacion.parroquia).count()
            mixtos = Matrimonio.objects.filter(fecha_sacramento__year=anio_actual, tipo_matrimonio='Mixto',
                                               parroquia=asignacion.parroquia).count()
            matrimonios = catolicos + mixtos
            form = ReporteSacramentosAnualForm(request.GET)
            if bautismos or eucaristias or confirmaciones or matrimonios:
                if form.is_valid():
                    html = render_to_string('reportes/reporte_anual_sacramentos.html',
                                            {'pagesize': 'A4', 'num_bautizos': num_bautizos, 'ninios1': ninios1,
                                             'ninios7': ninios7,
                                             'ninios': ninios, 'eucaristias': eucaristias,
                                             'confirmaciones': confirmaciones,
                                             'catolicos': catolicos, 'mixtos': mixtos, 'asignacion': asignacion,
                                             'cura': cura,
                                             'anio_actual': anio_actual, 'matrimonios': matrimonios, 'p': p},
                                            context_instance=RequestContext(request))
                    return generar_pdf(html)


                else:
                    messages.error(request, MENSAJE_ERROR)
                    ctx = {'form': form}
                # return render(request, template_name, ctx)
            else:
                messages.error(request, 'No hay sacramentos en este año')
                ctx = {'form': form}
        else:
            form = ReporteSacramentosAnualForm()
    # else:
    #     messages.error(request, 'El año tiene que ser de 4 digitos')
    #     ctx = {'form': form}

    ctx = {'form': form}
    return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.add_intencion', login_url='/login/',
                     raise_exception=permission_required)
@permission_required('sacramentos.change_intencion', login_url='/login/',
                     raise_exception=permission_required)
def reporte_intenciones(request):
    parroquia = request.session.get('parroquia')
    user = request.user
    if not parroquia:
        raise PermissionDenied
    tipo = request.GET.get('tipo')
    fecha_inicial = request.GET.get('fecha')
    fecha_final = request.GET.get('fecha_final')
    anio = request.GET.get('anio')
    hora = request.GET.get('hora')
    template_name = "reportes/reporte_intenciones_form.html"

    if tipo == 'dh':  # reporte diario por horas
        if fecha_inicial and hora:
            try:
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied
            intenciones = Intencion.objects.filter(fecha=fecha_inicial, hora=hora, parroquia=parroquia).order_by('hora')
            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=parroquia, periodos__estado=True)
            form = ReporteIntencionesForm(request.GET)

            if intenciones:
                suma = intenciones.aggregate(Sum('ofrenda'))['ofrenda__sum']

                if form.is_valid():
                    html = render_to_string('reportes/reporte_intenciones.html',
                                            {'pagesize': 'A4', 'intenciones': intenciones, 'parroquia': parroquia,
                                             'cura': cura, 'suma': suma, 'p': p, 'user': user},
                                            context_instance=RequestContext(request))
                    return generar_pdf(html)

                else:
                    messages.error(request, MENSAJE_ERROR)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
            else:
                messages.error(request, 'No hay intenciones en ha fecha ingresada')
                ctx = {'form': form}
                return render(request, template_name, ctx)

    if tipo == 'd':  # reporte diario
        if fecha_inicial:
            p = ParametrizaDiocesis.objects.all()
            intenciones = Intencion.objects.filter(fecha=fecha_inicial, parroquia=parroquia).order_by('hora')
            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=parroquia, periodos__estado=True)
            form = ReporteIntencionesForm(request.GET)

            if intenciones:
                suma = intenciones.aggregate(Sum('ofrenda'))['ofrenda__sum']

                if form.is_valid():
                    html = render_to_string('reportes/reporte_intenciones.html',
                                            {'pagesize': 'A4', 'intenciones': intenciones, 'parroquia': parroquia,
                                             'cura': cura, 'suma': suma, 'p': p, 'user': user},
                                            context_instance=RequestContext(request))
                    return generar_pdf(html)

                else:
                    messages.error(request, MENSAJE_ERROR)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)

            else:
                messages.error(request, 'No hay intenciones en la fecha ingresada')
                form.fields['fecha'].widget = forms.TextInput(attrs={'data-date-format': 'dd/mm/yyyy', 'type': 'date',
                                                                     'style': 'display:inline-block;'})
                ctx = {'form': form}
                return render(request, template_name, ctx)

    if tipo == 'r':  # reporte por rango de fechas

        if fecha_inicial and fecha_final:
            try:
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied

            start_date = datetime.strptime(fecha_inicial, "%Y-%m-%d").date()
            end_date = datetime.strptime(fecha_final, "%Y-%m-%d").date()

            intenciones = Intencion.objects.filter(fecha__range=[start_date, end_date],
                                                     parroquia=parroquia).order_by('hora')
            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=parroquia, periodos__estado=True)
            form = ReporteIntencionesForm(request.GET)
            if intenciones:
                if form.is_valid():

                    suma = intenciones.aggregate(Sum('ofrenda'))['ofrenda__sum']
                    html = render_to_string('reportes/reporte_intenciones.html',
                                            {'pagesize': 'A4', 'intenciones': intenciones, 'parroquia': parroquia,
                                             'cura': cura, 'suma': suma, 'p': p, 'user': user},
                                            context_instance=RequestContext(request))
                    return generar_pdf(html)

                else:
                    messages.error(request, MENSAJE_ERROR)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
            else:
                messages.error(request, 'No hay intenciones en ha fecha ingresada')
                ctx = {'form': form}
                return render(request, template_name, ctx)

    if tipo == 'h':  # reporte por fecha y horas

        if fecha_inicial and fecha_final and hora:
            try:
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied

            start_date = datetime.strptime(fecha_inicial, "%Y-%m-%d").date()
            end_date = datetime.strptime(fecha_final, "%Y-%m-%d").date()

            intenciones = Intencion.objects.filter(fecha__range=[start_date, end_date], hora=hora,
                                                     parroquia=parroquia).order_by('hora')
            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=parroquia, periodos__estado=True)
            form = ReporteIntencionesForm(request.GET)
            if intenciones:
                if form.is_valid():

                    suma = intenciones.aggregate(Sum('ofrenda'))['ofrenda__sum']
                    html = render_to_string('reportes/reporte_intenciones.html',
                                            {'pagesize': 'A4', 'intenciones': intenciones, 'parroquia': parroquia,
                                             'cura': cura, 'suma': suma, 'p': p, 'user': user},
                                            context_instance=RequestContext(request))
                    return generar_pdf(html)

                else:
                    messages.error(request, MENSAJE_ERROR)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
            else:
                messages.error(request, 'No hay intenciones en ha fecha ingresada')
                ctx = {'form': form}
                return render(request, template_name, ctx)

    if tipo == 'a':  # reporte anual
        if anio:
            try:
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied
            intenciones = Intencion.objects.filter(fecha__year=anio,
                                                     parroquia=parroquia).order_by('hora')
            suma = Intencion.objects.filter(fecha__year=anio,
                                              parroquia=parroquia).aggregate(Sum('ofrenda'))['ofrenda__sum']
            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=parroquia, periodos__estado=True)
            form = ReporteIntencionesForm(request.GET)
            if intenciones:
                if form.is_valid():
                    html = render_to_string('reportes/reporte_intenciones.html',
                                            {'pagesize': 'A4', 'intenciones': intenciones, 'parroquia': parroquia,
                                             'cura': cura, 'suma': suma, 'p': p},
                                            context_instance=RequestContext(request))
                    return generar_pdf(html)

                else:
                    messages.error(request, MENSAJE_ERROR)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
            else:
                messages.error(request, 'No hay intenciones en la fecha ingresada')
                ctx = {'form': form}
                return render(request, template_name, ctx)
    else:
        form = ReporteIntencionesForm()

    ctx = {'form': form}
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
    if request.method == 'POST':
        feligres = request.POST.get('feligres')
        tipo = request.POST.get('tipo')
        form = ReportePermisoForm(request.POST)
        if (tipo == 'Bautismo' and feligres):

            feligres = PerfilUsuario.objects.get(pk=feligres)
            print(feligres)
            try:
                asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                             periodos__estado=True)
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied

            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=asignacion.parroquia, periodos__estado=True)
            try:
                if Bautismo.objects.get(bautizado=feligres):
                    messages.error(request, 'El feligres tiene registrado un Bautismo')
                    queryset = PerfilUsuario.objects.filter(pk=feligres.pk)
                    form = ReportePermisoForm(queryset, request.POST)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
            except ObjectDoesNotExist:
                html = render_to_string('reportes/reporte_permiso.html',
                                        {'pagesize': 'A4', 'feligres': feligres, 'asignacion': asignacion, 'cura': cura,
                                         'tipo': tipo, 'p': p}, context_instance=RequestContext(request))
                return generar_pdf(html)


        elif (tipo == 'Primera Comunion' and feligres):

            feligres = PerfilUsuario.objects.get(id=feligres)
            try:
                asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                             periodos__estado=True)
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied

            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=asignacion.parroquia, periodos__estado=True)

            try:
                if Eucaristia.objects.get(feligres=feligres):
                    messages.error(request, 'El feligres tiene registrado una Eucaristia')
                    queryset = PerfilUsuario.objects.filter(pk=feligres.pk)
                    form = ReportePermisoForm(queryset, request.POST)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
            except ObjectDoesNotExist:
                html = render_to_string('reportes/reporte_permiso.html',
                                        {'pagesize': 'A4', 'feligres': feligres, 'asignacion': asignacion, 'cura': cura,
                                         'tipo': tipo, 'p': p},
                                        context_instance=RequestContext(request))
                return generar_pdf(html)


        elif (tipo == 'Confirmacion' and feligres):

            feligres = PerfilUsuario.objects.get(id=feligres)
            try:
                asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                             periodos__estado=True)
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied
            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=asignacion.parroquia, periodos__estado=True)
            try:
                if Confirmacion.objects.get(confirmado=feligres):
                    messages.error(request, 'El feligres tiene registrado una Confirmacion')
                    queryset = PerfilUsuario.objects.filter(pk=feligres.pk)
                    form = ReportePermisoForm(queryset, request.POST)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
            except ObjectDoesNotExist:
                html = render_to_string('reportes/reporte_permiso.html',
                                        {'pagesize': 'A4', 'feligres': feligres, 'asignacion': asignacion, 'cura': cura,
                                         'tipo': tipo, 'p': p},
                                        context_instance=RequestContext(request))
                return generar_pdf(html)


        elif tipo == 'Matrimonio' and feligres:

            feligres = PerfilUsuario.objects.get(id=feligres)
            try:
                asignacion = AsignacionParroquia.objects.get(persona__user=request.user,
                                                             periodos__estado=True)
                p = ParametrizaDiocesis.objects.all()
            except ObjectDoesNotExist:
                raise PermissionDenied
            cura = AsignacionParroquia.objects.get(persona__user__groups__name='Sacerdote',
                                                   parroquia=asignacion.parroquia, periodos__estado=True)

            if feligres.sexo == Item.objects.masculino():
                if Matrimonio.objects.filter(novio=feligres, vigente=True):
                    messages.error(request, 'El feligres tiene registrado un matrimonio vigente')
                    queryset = PerfilUsuario.objects.filter(pk=feligres.pk)
                    form = ReportePermisoForm(queryset, request.POST)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)

                else:
                    html = render_to_string('reportes/reporte_permiso.html',
                                            {'pagesize': 'A4', 'feligres': feligres, 'asignacion': asignacion,
                                             'cura': cura,
                                             'tipo': tipo, 'p': p}, context_instance=RequestContext(request))
                    return generar_pdf(html)
            else:
                if Matrimonio.objects.filter(novia=feligres, vigente=True):
                    messages.error(request, 'El feligres tiene registrado un matrimonio vigente')
                    queryset = PerfilUsuario.objects.filter(pk=feligres.pk)
                    form = ReportePermisoForm(queryset, request.POST)
                    ctx = {'form': form}
                    return render(request, template_name, ctx)
                else:
                    html = render_to_string('reportes/reporte_permiso.html',
                                            {'pagesize': 'A4', 'feligres': feligres, 'asignacion': asignacion,
                                             'cura': cura,
                                             'tipo': tipo, 'p': p}, context_instance=RequestContext(request))
                    return generar_pdf(html)

    else:
        form = ReportePermisoForm()
        ctx = {'form': form}
        return render(request, template_name, ctx)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_parroquia', login_url='/login/',
                     raise_exception=permission_required)
def reporte_parroquias_sacerdotes(request, pk):
    persona = User.objects.get(pk=request.user.pk)
    parroquia = get_object_or_404(Parroquia, pk=pk)

    periodos = PeriodoAsignacionParroquia.objects.filter(asignacion__parroquia=parroquia,
                                                         asignacion__persona__user__groups__name='Sacerdote')
    try:
        p = ParametrizaDiocesis.objects.all()
    except ObjectDoesNotExist:
        raise PermissionDenied

    print(periodos)
    html = render_to_string('reportes/reporte_parroquia_sacerdote.html', {'pagesize': 'A4',
                                                                          'parroquia': parroquia, 'periodos': periodos,
                                                                          'persona': persona, 'p': p},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


@login_required(login_url='/login/')
@permission_required('sacramentos.change_sacerdote', login_url='/login/',
                     raise_exception=permission_required)
def reporte_sacerdotes_parroquias(request, pk):
    persona = User.objects.get(pk=request.user.pk)
    cura = get_object_or_404(PerfilUsuario, pk=pk)
    periodos = PeriodoAsignacionParroquia.objects.filter(asignacion__persona=cura)
    p = ParametrizaDiocesis.objects.all()
    print(periodos)
    html = render_to_string('reportes/reporte_sacerdote_parroquia.html', {'pagesize': 'A4',
                                                                          'periodos': periodos, 'persona': persona,
                                                                          'cura': cura, 'p': p},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


# exportar a csv los logs

@login_required(login_url='/login/')
@permission_required('admin.change_logentry', login_url='/login/',
                     raise_exception=permission_required)
def exportar_csv_logs(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="logs.csv"'
    writer = csv.writer(response)
    logs = LogEntry.objects.all()
    writer.writerow(
        ['id', 'action_time', 'user_id', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message'])
    for log in logs:
        writer.writerow([log.id, log.action_time, log.user, log.content_type, log.object_id, encode(log.object_repr),
                         log.action_flag, encode(log.change_message)])
    return response

# para poder exportar a csv con utf-8

def encode(text):
    return text.encode('utf-8')


@login_required(login_url='/login/')
def redireccionar(request):
    cont = 0
    url = ''

    if request.user.has_perm('sacramentos.add_feligres'):
        cont = cont + 1
        url = '/usuario/'

    if request.user.has_perm('sacramentos.add_administrador'):
        cont = cont + 1
        url = '/administrador/'
    if request.user.has_perm('sacramentos.add_sacerdote'):
        cont = cont + 1
        url = '/sacerdote/'

    if request.user.has_perm('sacramentos.add_asignarsecretaria'):
        cont = cont + 1
        url = '/asignar/secretaria/'

    if cont == 1:
        return HttpResponseRedirect(url)
    else:
        return render(request, 'personas.html')


@login_required(login_url='/login/')
def redireccionar_parametros(request):
    cont = 0
    url = ''

    if request.user.has_perm('sacramentos.add_parametrizadiocesis'):
        cont = cont + 1
        url = '/parametriza/add/'

    if request.user.has_perm('sacramentos.add_parametrizaparroquia'):
        cont = cont + 1
        url = '/parametriza/parroquia/add/'

    if cont == 1:
        return HttpResponseRedirect(url)
    else:
        return render(request, 'parametros.html')


class IglesiaListView(PaginacionMixin, ListView):
    model = Iglesia
    template_name = 'iglesia/iglesia_list.html'
    paginate_by = 10

    def get_queryset(self):
        parroquia = self.request.session.get('parroquia')
        if parroquia:
            # return Iglesia.objects.filter(parroquia=parroquia).extra(select={'nombre': 'lower(nombre)'}).order_by('nombre')
            name = self.request.GET.get('q', '')
            if (name != ''):
                return Iglesia.objects.filter(parroquia=parroquia, nombre__icontains=name).order_by('-principal',
                                                                                                    'nombre')
            else:
                return Iglesia.objects.filter(parroquia=parroquia).order_by('-principal', 'nombre')
        else:
            raise PermissionDenied


class IglesiaCreateView(CreateView):
    model = Iglesia
    template_name = 'iglesia/iglesia_form.html'
    success_url = reverse_lazy('iglesia_list')
    form_class = IglesiaForm

    def get_form_kwargs(self):
        kwargs = super(IglesiaCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, MENSAJE_EXITO_CREACION)
        return super(IglesiaCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, MENSAJE_ERROR)
        return super(IglesiaCreateView, self).form_invalid(form)


class IglesiaUpdateView(UpdateView):
    model = Iglesia
    template_name = 'iglesia/iglesia_form.html'
    success_url = reverse_lazy('iglesia_list')
    form_class = IglesiaForm

    def get_form_kwargs(self):
        kwargs = super(IglesiaUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, MENSAJE_EXITO_ACTUALIZACION)
        return super(IglesiaUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, MENSAJE_ERROR)
        return super(IglesiaUpdateView, self).form_invalid(form)







