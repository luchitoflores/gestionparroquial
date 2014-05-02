# -*- coding:utf-8 -*-

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
def consulta_paginada(pagina_actual):
	page_obj = ''
	try:
		page_obj = paginator.page(pagina_actual)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
		# pagina_actual = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	return page_obj

	
	



	
			
	


