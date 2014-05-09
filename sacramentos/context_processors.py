from django.core.urlresolvers import reverse_lazy
from .models import ParametrizaDiocesis, ParametrizaParroquia

def parametros_diocesis(request):
	parametros = ParametrizaDiocesis.objects.all()
	if parametros:
		return {'parametros': parametros[0]}
	else:
		return {'parametros': ''}

def parametros_parroquiales(request):
	parametros = ParametrizaParroquia.objects.all()
	if parametros:
		return {'parametros_parroquia': parametros[0]}
	else:
		return {'parametros_parroquia': ''}

def menu(request):
	menu = {'menu': [
	{'nombre': 'Iglesia', 'url': reverse_lazy('iglesia_list')},
	{'nombre': 'Ciudades', 'submenu': [
		{'nombre': 'Provincias','url':reverse_lazy('provincia_list')},
		{'nombre': 'Cantones','url':reverse_lazy('canton_list')},
		{'nombre': 'Parroquias','url':reverse_lazy('parroquia_list')},
		]},
	{'nombre': 'Intenciones', 'url': reverse_lazy('intencion_list')},
	]}

	return menu