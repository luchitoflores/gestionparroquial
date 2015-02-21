__author__ = 'LFL'

from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^catalogo/$', TemplateView.as_view(template_name='catalogo/catalogo.html'), name='catalogo'),
    url(r'^item/$', TemplateView.as_view(template_name='catalogo/item.html'), name='item'),
    url(r'^parametros/$', TemplateView.as_view(template_name='catalogo/parametro.html'), name='parametros'),
    url(r'^modulo/$', TemplateView.as_view(template_name='catalogo/modulo.html'), name='modulo'),
    url(r'^funcionalidad/$', TemplateView.as_view(template_name='catalogo/funcionalidad.html'), name='funcionalidad'),

)
