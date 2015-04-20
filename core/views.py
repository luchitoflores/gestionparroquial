# -*- coding:utf-8 -*-

import datetime
import unicodedata
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import SearchLogsForm


class PaginacionMixin(object):

    def get_context_data(self, **kwargs):
        context = super(PaginacionMixin, self).get_context_data(**kwargs)
        numero_paginas = context['paginator'].num_pages
        pagina_actual = context['page_obj'].number

        if numero_paginas > 5 :
            resta = numero_paginas - pagina_actual

            if pagina_actual <= 2:
                context['rango'] = [x for x in range(1,6)]
            else:
                if resta > 1:
                    context['rango'] = [pagina_actual-2, pagina_actual-1, pagina_actual, pagina_actual+1, pagina_actual+2]
                elif resta <= 1:
                    context['rango'] = [x for x in range(numero_paginas-4,numero_paginas+1)]
        elif numero_paginas <= 5:
            context['rango'] = [x for x in range(1,numero_paginas+1)]

        context['q'] = self.request.GET.get('q', '')
        return context


class PaginacionLogsMixin(object):

    def get_context_data(self, **kwargs):
        context = super(PaginacionLogsMixin, self).get_context_data(**kwargs)
        numero_paginas = context['paginator'].num_pages
        pagina_actual = context['page_obj'].number

        if numero_paginas > 5 :
            resta = numero_paginas - pagina_actual

            if pagina_actual <= 2:
                context['rango'] = [x for x in range(1,6)]
            else:
                if resta > 1:
                    context['rango'] = [pagina_actual-2, pagina_actual-1, pagina_actual, pagina_actual+1, pagina_actual+2]
                elif resta <= 1:
                    context['rango'] = [x for x in range(numero_paginas-4,numero_paginas+1)]
        elif numero_paginas <= 5:
            context['rango'] = [x for x in range(1,numero_paginas+1)]

        context['username'] = self.request.GET.get('username', '')
        context['action_flag'] = self.request.GET.get('action_flag', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context


class BusquedaMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BusquedaMixin, self).get_context_data(**kwargs)
        numero_paginas = context['paginator'].num_pages
        pagina_actual = context['page_obj'].number

        if numero_paginas > 5 :
            resta = numero_paginas - pagina_actual

            if pagina_actual <= 2:
                context['rango'] = [x for x in range(1,6)]
            else:
                if resta > 1:
                    context['rango'] = [pagina_actual-2, pagina_actual-1, pagina_actual, pagina_actual+1, pagina_actual+2]
                elif resta <= 1:
                    context['rango'] = [x for x in range(numero_paginas-4,numero_paginas+1)]
        elif numero_paginas <= 5:
            context['rango'] = [x for x in range(1,numero_paginas+1)]

        context['q'] = self.request.GET.get('q', '')
        #context['modelo'] = self.model._meta.object_name
        return context

    def get_queryset(self):
        name = self.request.GET.get('q', '')

        if (name != ''):
            object_list = self.model.objects.filter(nombre__icontains = name).order_by('nombre')
        else:
            object_list = self.model.objects.all().order_by('nombre')
        return object_list


class BusquedaPersonaMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BusquedaPersonaMixin, self).get_context_data(**kwargs)
        numero_paginas = context['paginator'].num_pages
        pagina_actual = context['page_obj'].number

        if numero_paginas > 5 :
            resta = numero_paginas - pagina_actual

            if pagina_actual <= 2:
                context['rango'] = [x for x in range(1,6)]
            else:
                if resta > 1:
                    context['rango'] = [pagina_actual-2, pagina_actual-1, pagina_actual, pagina_actual+1, pagina_actual+2]
                elif resta <= 1:
                    context['rango'] = [x for x in range(numero_paginas-4,numero_paginas+1)]
        elif numero_paginas <= 5:
            context['rango'] = [x for x in range(1,numero_paginas+1)]

        context['q'] = self.request.GET.get('q', '')
        #context['modelo'] = self.model._meta.object_name
        return context

    def get_queryset(self):
        name = self.request.GET.get('q', '')

        if (name != ''):
            object_list = self.model.objects.filter(user__first_name__icontains = name).order_by('user__last_name')
        else:
            object_list = self.model.objects.all().order_by('user__last_name')
        return object_list

def quitar_tildes(palabra):
    import unicodedata
    palabra = ''.join((c for c in unicodedata.normalize('NFD', unicode(palabra)) if unicodedata.category(c) != 'Mn'))
    return palabra



#Métodos para contruir una consulta paginada dentro de una tabla

def consulta_con_query(consultar_todos, consulta_con_busqueda, query):
    if query:
        queryset = consulta_con_busqueda
    else:
        queryset = consultar_todos
    return queryset

# Método para convertir un queryset en un objeto Paginator
def paginador(queryset):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    return Paginator(queryset, 10)

# Método que permite ver si un QuerySet tiene más de una página
# El número total de páginas se lo obtiene a partir del paginador Ej:
# numero_total_paginas = paginator.num_pages
def es_paginado(numero_total_paginas):
    if numero_total_paginas > 1:
        is_paginated = True
    else:
        is_paginated = False
    return is_paginated

# Método que devuelve el rango de páginas que se mostrarán en el template
# La página actual es igual a page = request.GET.get('page')
def rango_paginas(numero_total_paginas, pagina_actual):
    if numero_total_paginas > 5 :
        resta = numero_total_paginas - pagina_actual

        if pagina_actual <= 2:
            return [x for x in range(1,6)]
        else:
            if resta > 1:
                return [pagina_actual-2, pagina_actual-1, pagina_actual, pagina_actual+1, pagina_actual+2]
            elif resta <= 1:
                return [x for x in range(numero_total_paginas-4,numero_total_paginas+1)]
    elif numero_total_paginas <= 5:
        return [x for x in range(1,numero_total_paginas+1)]

# Devuelve el queryset paginado de acuerdo a la página dada
# def consulta_paginada(pagina_actual):
#     page_obj = ''
#     try:
#         page_obj = paginator.page(pagina_actual)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#         # pagina_actual = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#
#     return page_obj

def catalogo_view(request):
    return HttpResponseRedirect('/catalogo/')


class LogListView(PaginacionLogsMixin, ListView):
    model = LogEntry
    template_name = 'seguridad/log_list.html'
    paginate_by = 10

    def get_queryset(self):
        username = self.request.GET.get('username', '')
        action_flag = self.request.GET.get('action_flag', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
            queryset = LogEntry.objects.filter(action_time__range=[start_datetime, end_datetime])

            if username:
                username = ''.join((c for c in unicodedata.normalize('NFD', unicode(username)) if unicodedata.category(c) != 'Mn'))
                queryset = queryset.filter(user__username__icontains=username)
            if action_flag:
                queryset = queryset.filter(action_flag=action_flag)

            return queryset.order_by('user__username', '-action_time')

        else:
            return LogEntry.objects.all().order_by('user__username', '-action_time')

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('admin.change_logentry', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(LogListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LogListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['publisher'] = "prueba"
        return context

class LogListView2(PaginacionLogsMixin, ListView):
    model = LogEntry
    template_name = 'seguridad/log_list2.html'
    paginate_by = 10

    def get_queryset(self):
        username = self.request.GET.get('username', '')
        action_flag = self.request.GET.get('action_flag', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
            queryset = LogEntry.objects.filter(action_time__range=[start_datetime, end_datetime])

            if username:
                username = ''.join((c for c in unicodedata.normalize('NFD', unicode(username)) if unicodedata.category(c) != 'Mn'))
                queryset = queryset.filter(user__username__icontains=username)
            if action_flag:
                queryset = queryset.filter(action_flag=action_flag)

            return queryset.order_by('user__username', '-action_time')

        else:
            return LogEntry.objects.all().order_by('user__username', '-action_time')

    @method_decorator(login_required(login_url='/login/'))
    @method_decorator(permission_required('admin.change_logentry', login_url='/login/',
                                          raise_exception=permission_required))
    def dispatch(self, *args, **kwargs):
        return super(LogListView2, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LogListView2, self).get_context_data(**kwargs)
        # Add in the publisher
        context['publisher'] = "prueba"
        return context
