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
