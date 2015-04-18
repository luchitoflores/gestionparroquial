from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from sacramentos import urls as sacramentos_urls 
from usuarios import urls as usuarios_urls
from core import urls as core_urls
from django.utils.functional import curry
from django.views.defaults import *

from rest_framework import routers

from core.serializers import (CatalogoViewSet, ItemViewSet, ItemsPaginatedViewSet, ParametroViewSet,
                              FuncionalidadViewSet, ModuloViewSet, GroupViewSet, PermissionViewSet, LogsSearchListAPIView)

admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'catalogo', CatalogoViewSet)
router.register(r'item', ItemViewSet)
router.register(r'itemspaginados', ItemsPaginatedViewSet)
router.register(r'parametro', ParametroViewSet)
router.register(r'modulo', ModuloViewSet)
router.register(r'funcionalidad', FuncionalidadViewSet)
router.register(r'grupo', GroupViewSet)
router.register(r'permiso', PermissionViewSet)


urlpatterns = patterns('',
    url(r'^api-auth/log/', LogsSearchListAPIView.as_view()),
    url(r'^api-auth/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework') ),
    url(r'^', include(sacramentos_urls)),
    url(r'^', include(usuarios_urls)),
    url(r'^', include(core_urls)),
)

handler500 = curry(server_error, template_name='500.html')
handler404 = curry(page_not_found, template_name='404.html')
handler403 = curry(permission_denied, template_name='403.html')
