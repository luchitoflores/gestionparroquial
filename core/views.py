# Create your views here.

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