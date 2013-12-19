from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from sacramentos import urls as sacramentos_urls 
from home import urls as home_urls
from usuarios import urls as usuarios_urls
from ciudades import urls as ciudades_urls
from django.utils.functional import curry
from django.views.defaults import *

admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ekklesia.views.home', name='home'),s
    # url(r'^ekklesia/', include('ekklesia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(sacramentos_urls)),
    url(r'^', include(home_urls)),
    url(r'^', include(usuarios_urls)),
    url(r'^', include(ciudades_urls)),
)

handler500 = curry(server_error, template_name='500.html')
handler404 = curry(page_not_found, template_name='404.html')
handler403 = curry(permission_denied, template_name='403.html')
