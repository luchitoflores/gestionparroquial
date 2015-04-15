__author__ = 'LFL'

from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView

from .views import LogListView


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


urlpatterns = patterns('',
                       url(r'^catalogo/$', login_required(TemplateView.as_view(template_name='catalogo/catalogo.html'),
                                                          login_url='/login/'),
                           name='catalogo'),
                       url(r'^item/$', login_required(TemplateView.as_view(template_name='catalogo/item.html'),
                                                      login_url='/login/'), name='item'),
                       url(r'^parametros/$',
                           login_required(TemplateView.as_view(template_name='catalogo/parametro.html'),
                                          login_url='/login/'),
                           name='parametros'),
                       url(r'^modulo/$', login_required(TemplateView.as_view(template_name='catalogo/modulo.html'),
                                                        login_url='/login/'), name='modulo'),
                       url(r'^funcionalidad/$',
                           login_required(TemplateView.as_view(template_name='catalogo/funcionalidad.html'),
                                          login_url='/login/'),
                           name='funcionalidad'),
                       url(r'^log/$', login_required(LogListView.as_view(), login_url='/login/'), name='log_list'),
                       # Urls include para angular js
                       url(r'include/messages/$', TemplateView.as_view(template_name='includes/messages.html'),
                           name='messages'),
)
