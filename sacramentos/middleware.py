from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation
from sacramentos.models import PeriodoAsignacionParroquia, Configuracion
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect


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
                parroquia = PeriodoAsignacionParroquia.objects.get(asignacion__persona__user__id=request.user.id,
                                                                   estado=True).asignacion.parroquia
                if parroquia:
                    request.session["parroquia"] = parroquia
            except ObjectDoesNotExist:
                pass


class ConfiguracionMiddleware(object):
    def process_request(self, request):
        usuario = request.user
        if usuario.is_authenticated():  # and usuario.groups.filter(name='Administrador'):
            parroquia = request.session.get("parroquia")
            if parroquia:
                try:
                    configuracion = Configuracion.objects.all()[:1].get()
                    if configuracion:
                        if configuracion[0].libro_bautismo:
                            return None
                        else:
                            if request.path == reverse_lazy('configuracion_inicial'): # esto evita que se haga un bucle de redireccion
                                return None
                            else:
                                return redirect('configuracion_inicial')
                except:
                    if request.path == reverse_lazy('configuracion_inicial'):
                        return None
                    else:
                        return redirect('configuracion_inicial')
            else:
                return None




