# Create your views here.


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

		context['now'] = numero_paginas 
		context['pagina_actual'] = pagina_actual
		context['q'] = self.request.GET.get('q', '')
		return context

	def get_queryset(self):
		print self.args
		name = self.request.GET.get('q', '')
		print "valor de name"
		print name
		
		if (name != ''):
			object_list = self.model.objects.filter(nombre__icontains = name)
		else:
			object_list = self.model.objects.all()
		return object_list
