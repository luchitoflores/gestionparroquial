__author__ = 'LFL'

from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import LogListView

from django.http import HttpResponseBadRequest

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

urlpatterns = patterns('',
                       url(r'^catalogo/$', TemplateView.as_view(template_name='catalogo/catalogo.html'),
                           name='catalogo'),
                       url(r'^item/$', TemplateView.as_view(template_name='catalogo/item.html'), name='item'),
                       url(r'^parametros/$', TemplateView.as_view(template_name='catalogo/parametro.html'),
                           name='parametros'),
                       url(r'^modulo/$', TemplateView.as_view(template_name='catalogo/modulo.html'), name='modulo'),
                       url(r'^funcionalidad/$', TemplateView.as_view(template_name='catalogo/funcionalidad.html'),
                           name='funcionalidad'),
                       url(r'^log/$', LogListView.as_view(), name='log_list'),
                       # Urls include para angular js
                       url(r'include/messages/$', TemplateView.as_view(template_name='includes/messages.html'),
                           name='messages'),
)
