from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation
from sacramentos.models import PeriodoAsignacionParroquia

class AdminLocaleURLMiddleware:
	def process_request(self, request):
		if request.path.startswith('/admin'):
			request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
			translation.activate(request.LANG)
			request.LANGUAGE_CODE = request.LANG


class ParroquiaSessionMiddleware(object):
	def process_request(self, request):
		if request.user.is_authenticated():
			try:
				parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user__id=request.user.id, estado=True).asignacion.parroquia
				if parroquia:
					request.session["parroquia"] = parroquia 
			except ObjectDoesNotExist:
				pass

	# def process_exception(self, request, exception):
	# 	pass
