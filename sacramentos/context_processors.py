from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy

from .models import ParametrizaDiocesis, ParametrizaParroquia


def parametros_diocesis(request):
    try:
        parametros = ParametrizaDiocesis.objects.get(pk=1)
        return {'parametros': parametros}
    except ObjectDoesNotExist:
        return {'parametros': ''}


def parametros_parroquiales(request):
    parametros = ParametrizaParroquia.objects.all()
    if parametros:
        return {'parametros_parroquia': parametros[0]}
    else:
        return {'parametros_parroquia': ''}

