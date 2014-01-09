# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Provincia, Canton,Parroquia, Direccion

	

class ParroquiasAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'canton__nombre')

admin.site.register(Provincia)
admin.site.register(Canton)
admin.site.register(Parroquia, ParroquiasAdmin)
admin.site.register(Direccion)