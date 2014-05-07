# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import (
	ProvinciaCreate, ProvinciaUpdate, ProvinciaList, ProvinciaDelete,
	CantonCreate, CantonUpdate, CantonList, CantonDelete,
	ParroquiaCreate, ParroquiaUpdate, ParroquiaList, ParroquiaDelete

	)
from django.contrib.auth.decorators import login_required
from .rest import (
	ProvinciaCreateRead,ProvinciaCreateReadUpdateDelete,
	CantonCreateRead,CantonCreateReadUpdateDelete,
	ParroquiaCreateRead, ParroquiaCreateReadUpdateDelete,
	seleccionar_ciudades, direccion_create_view)



urlpatterns = patterns('ciudades.views',
		
	url(r'^ciudades/crear/provincia/$', ProvinciaCreate.as_view(), name='provincia_create'),
	url(r'^ciudades/provincia/(?P<pk>\d+)/$', ProvinciaUpdate.as_view(), name='provincia_update'),
	url(r'^ciudades/provincia/(?P<pk>\d+)/delete/$', ProvinciaDelete.as_view(), name='provincia_delete'), 
	url(r'^ciudades/provincia/$', ProvinciaList.as_view() , name='provincia_list'),
	url(r'^ciudades/crear/canton/$', CantonCreate.as_view(), name='canton_create'),
	url(r'^ciudades/canton/(?P<pk>\d+)/$', CantonUpdate.as_view(), name='canton_update'),
	url(r'^ciudades/canton/(?P<pk>\d+)/delete/$', CantonDelete.as_view(), name='canton_delete'), 
	url(r'^ciudades/canton/$', CantonList.as_view() , name='canton_list'),
	url(r'^ciudades/crear/parroquia/$', ParroquiaCreate.as_view(), name='parroquiacivil_create'),
	url(r'^ciudades/parroquia/(?P<pk>\d+)/$', ParroquiaUpdate.as_view(), name='parroquiacivil_update'),
	url(r'^ciudades/parroquia/(?P<pk>\d+)/delete/$', ParroquiaDelete.as_view(), name='parroquiacivil_delete'), 
	url(r'^ciudades/parroquia/$', ParroquiaList.as_view() , name='parroquiacivil_list'),
	url(r'^ciudades/crear/direccion//$', direccion_create_view),
	url(r'^api/ciudades/crear/provincia/$', ProvinciaCreateRead.as_view()),
	url(r'^api/ciudades/provincia/$', ProvinciaCreateReadUpdateDelete.as_view()),
	url(r'^api/ciudades/crear/canton/$', CantonCreateRead.as_view()),
	url(r'^api/ciudades/canton/$', CantonCreateReadUpdateDelete.as_view()),
	url(r'^api/ciudades/crear/parroquia/$', ParroquiaCreateRead.as_view()),
	url(r'^api/ciudades/parroquia/$', ParroquiaCreateReadUpdateDelete.as_view()),
	url(r'^api/ciudades/select/$', seleccionar_ciudades),

	url(r'^ciudades/$', TemplateView.as_view(template_name='ciudades.html'), 
		name='ciudades'),
)