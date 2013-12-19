from django.conf.urls import url, patterns
from .views import (GroupList, GroupCreate, GroupUpdate, 
login_view, logout_view, change_password_view, send_email_view)
from django.views.generic import TemplateView 



urlpatterns = patterns ('',
	url(r'^login/$', login_view, name='login'),
    # url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    # url(r'^permission_denied/$', TemplateView.as_view(template_name='permission_denied.html'), name='permission_denied'),
    url(r'^logout/$', logout_view , name='logout'), 
    url(r'^password_change/$', change_password_view , name='password_change'),
    url(r'^send/email/$', send_email_view , name='send_email'), 
    url(r'^group/add/$', GroupCreate.as_view(), name='group_create'),
    url(r'^group/$', GroupList.as_view(), name='group_list'),
    url(r'^group/(?P<pk>\d+)/$', GroupUpdate.as_view(), name='group_update'),
)